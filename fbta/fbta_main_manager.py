import copy
import time, datetime
from typing import List, Optional

import pymongo

from fbta_configs import FBTAConfigs
from fbta_settings import FBTASettings
from fbta_difftime import FBTADifftime
from fbta_global_database_manager import FBTADBManager
from fbta_main_worker import FBTAMainWorker
from fbta_node_master import FBTANodeMaster
from fbta_statistic import FBTAStatistic
from fbta_timer import FBTATimer
from fbta_log import log

"""
คลาส global จะใช้วิธีการสืบทอดอำนาจมืด คลาย Thread เลย โค๊ตจะได้สวยๆ
"""

from abc import ABCMeta, abstractmethod


class FBTAMainManager(metaclass=ABCMeta):
    def __init__(self, node_master: FBTANodeMaster,
                 db_collection_name,
                 slave_class_name: classmethod):

        self.say_hello_time = time.time()
        self.__slave_class_name = slave_class_name

        self.__timer = FBTATimer()

        self.__node_master = node_master
        self.__settings = self.__node_master.settings
        self.__configs = self.__node_master.configs

        self.__db = FBTADBManager(self.settings.db_name, db_collection_name)
        self.__stat = FBTAStatistic()
        self.__stat.history_time_global_start = time.time()

        self.__check_init_worker_is_ready = True

        self.__workers = []

        self.__constant_list = 2

        self.__big_loop_time = None
        self.__time_big_loop_report_time = 10

        self.__browser = None

        self.__initSettings()

    @property
    def stat(self) -> FBTAStatistic:
        return self.__stat

    @property
    def db(self) -> FBTADBManager:
        return self.__db

    @property
    def settings(self) -> FBTASettings:
        return self.__settings

    @property
    def configs(self) -> FBTAConfigs:
        return self.__configs

    @property
    def workers(self) -> List[Optional[FBTAMainWorker]]:
        return self.__workers

    @workers.setter
    def workers(self, slave):
        self.__workers = slave

    @workers.deleter
    def workers(self):
        self.__workers = []

    @abstractmethod
    def stop_main_condition(self) -> bool:
        pass

    def __run_cluster(self):
        for workser in self.workers:
            workser.setDaemon(False)
            workser.start()

    def _main(self):
        self.__create_workers(self.__slave_class_name)
        self.__run_cluster()

        self.__method_wait_worker_until_ready()
        log(':mManage: ( _)0*´¯`·.¸.·´¯`°Q(_ )  Start Main Manager')

        self.__init_time_event()

        while True:
            self.__method_addDataToList()

            __stopCouter = self.__method__addJobs()

            self.__show_all_waiting_job()

            if self.__stopCounter >= self.db.clusters_num:
                log(':mManage:  END LOOP')
                break

            if not self.__method_all_alive():
                log(':mManage:  End loop by thread dead')
                break

            self.__method_say_hello()

            self.__method_loop_big_reporter()
        self.__method_loop_big_report_show(0)

        self.__endThread()

    def __method_loop_big_reporter_time_switching(self):
        c = (self.db.db_index - self.db.clusters_num)
        cal = c if c >= 0 else 0
        if cal == 1 and not self.__big_loop_time:
            self.__big_loop_time = time.time()
        if cal > 1 and self.__big_loop_time:
            # print(':mMaanger:', time.time(), self.__big_loop_time)
            avr = int((time.time() - self.__big_loop_time)) / cal

            if avr < self.__time_big_loop_report_time:
                return self.__time_big_loop_report_time
            elif avr > 3 * self.__time_big_loop_report_time:
                return 3 * self.__time_big_loop_report_time
            else:
                return avr
        return self.__time_big_loop_report_time

    def __method_loop_big_reporter(self):
        time_of_big_loop = self.__method_loop_big_reporter_time_switching()
        if self.__timer.is_time('big_loop_report', time_of_big_loop):
            self.__method_loop_big_report_show(time_of_big_loop)
            self.__timer.update('big_loop_report')

    def __method_loop_big_report_show(self, loop_time):
        num_docs_now = len(self.db.docs_list)
        str = (f"\n---------------------\n"
               f"\t>> DocsLen  : {num_docs_now}\n"
               f"\t>> Index    : {self.db.db_index} / {self.db.current_num}\n"
               f"\t>> TimeNow  : {time.time()} ({datetime.datetime.now()})\n"
               f"\t>> Loopshow : {loop_time}   \n"
               f"\t>> FromStart: {FBTADifftime.printTimeDiff(self.__stat.history_time_global_start)}   \n"
               f"-----------------------\n"
               )

        log(str)

    def __clusters_cal_limit(self):
        cluster_num = self.__settings.cluster_num
        cluster_num_limit = self.__settings.cluster_limit
        return cluster_num if cluster_num <= cluster_num_limit else cluster_num_limit

    def __clusters_cal_all(self):
        clusters_num = self.__clusters_cal_limit()
        cards_num = self.__db.getCurrentCollection_num()

        self.db.clusters_num = cards_num if cards_num < clusters_num else clusters_num

    def __initSettings(self):
        self.db.docs_num = self.__db.getCurrentCollection_num()

        self.__clusters_cal_all()
        self.__printSettings()

    def __printSettings(self):
        settings = {
            'Cluster Num': self.db.clusters_num,
            'DB Index': self.db.docs_num
        }

        log('----- Settings ------')
        for key in settings:
            log(key, '=', settings[key])
        log('---------------------')

    def __create_workers(self, class_name):
        log(f':mMange: ■■■■■■■ Create Worker with [{self.db.clusters_num}] Clusters')
        for worker_id in range(self.db.clusters_num):
            self.workers.append(class_name(self.__node_master, self.db))
            self.__create_workers_method(class_name, worker_id)

    def __create_workers_method(self, class_name, worker_id):
        self.workers[worker_id].slave_name = str(worker_id)
        self.workers[worker_id].name = 'Slave-' + str(worker_id)
        self.workers[worker_id].slave_class_name = str(class_name.__name__)

    def __method_wait_worker_until_ready(self):
        while self.__check_init_worker_is_ready:
            a = [worker.is_ready for worker in self.workers]
            if all(a):
                log(':mMange: Worker all ready')
                self.__check_init_worker_is_ready = False
                break
            # print(f'wait util ready {time.time()} , {a}')

    def __show_all_waiting_job(self):
        if all([w.is_waiting_job() for w in self.workers]):
            log(
                f':mMange: ■■■■■■■ all waiting job index[{self.db.db_index}]  stopCouter[{self.__stopCounter}] '
                f'lenDocs[{len(self.db.docs_list)}]')

    def __method__addJobs(self):
        time.sleep(0.1)
        self.__stopCounter = 0

        for worker_id, worker in enumerate(self.workers):
            if worker:
                if worker.isErrorFatal:
                    log(':mMange: ■■■■■■■ ERROR EXIT ■■■■■■■', worker)
                    exit()

                if worker.is_waiting_job():
                    if self.db.docs_list:
                        jobs = self.db.docs_list.pop(0)
                        self.db.docs_list_waiting.append(
                            {'jid': str(jobs['_id']), 'time': time.time(), 'worker': worker.name,
                             'worker-id': worker_id})

                        worker.add_job(jobs)

                        self.__stat.worker_couter_docs += 1
                    else:
                        self.__method_check_worker_stop(worker)
                self.__method_remove_old_waiting_list(worker.get_last_job_finshed())
            else:
                print(f'mMange:{datetime.datetime.now()} Some Worker will be INIT please wait')
                self.__method_wait_worker_until_ready()
                print('mManage: OK Worker all run let\'s go')

    def __method_remove_old_waiting_list(self, id):
        search_index = self.__find_time(self.db.docs_list_waiting, 'jid', str(id))
        if search_index >= 0:
            remove = self.db.docs_list_waiting.pop(search_index)
            log(f':mMange: Remove from WAITING_LIST [{id}] index [{search_index}] '
                f'from {remove.get("worker", "NAN_WORKER")} in '
                f'{len(self.db.docs_list_waiting)} @ {remove.get("time", "non_naja")}')

    def __method_say_hello(self):
        if time.time() - self.say_hello_time > 5:
            for index, worker in enumerate(self.workers):
                if worker.sos_signal:
                    print(f':mManage: Manger send restart browser to [{worker.name}]')
                    old_job = copy.deepcopy(worker.download_current.get())
                    worker.restart_browser()
                    self.__method_wait_worker_until_ready()
                    if old_job:
                        worker.add_job(old_job)
            print(f'==================== SAY HELLO '
                  f'{[w.is_alive() for w in self.workers]} '
                  f'{[w.name for w in self.workers]}')
            self.__method_check_waiting_list()
            self.say_hello_time = time.time()

    def __method_check_waiting_list(self):
        for dw in self.db.docs_list_waiting:
            timeout_normal = time.time() - dw.get('time') > self.configs.timeout_waiting_list
            if timeout_normal:
                timeout_is_real = False
                try:
                    timeout_is_real = self.workers[dw.get('worker-id')].is_end()
                except:
                    pass
                if timeout_is_real:
                    print(f':mManage: Detect Worker [{dw.get("worker")}] spend more time (TIMEOUT) '
                          f'since [{time.time() - dw.get("time", 0)}] ago')
                    self.workers[dw.get('worker-id')].restart_browser()

    def __method_check_worker_stop(self, worker):
        # Check IS STOP cluster REALLY
        self.__stopCounter = 0
        if self.db.db_index >= self.db.getCurrentCollection_num():
            if not worker.is_end():
                log(f':mManage: manager send end job to {worker.name}')
            worker.end_job()
            if worker.is_end():
                self.__stopCounter += 1

    def __method_check_worker_is_respond(self):
        return self.db.docs_list_waiting

    def __method_addDataToList(self):
        num_fill_list = self.__add_docs_cursor_to_list()
        if num_fill_list > 0:
            log(f':mManger:\t >> Add Docs to list = {num_fill_list}')
            isShouldGetDocsInDBReturn = False
            return isShouldGetDocsInDBReturn
        return False

    def __method_stop_add_docs_to_list_condition(self):
        return self.db.db_index >= self.db.getCurrentCollection_num()

    def __method_all_alive(self):
        p = [w.is_end() for w in self.workers]
        a = all(p)
        if a:
            log(f'\n:mMange: xxxxxx ALL DIED xxxxxx\n'
                f':mMange: x {p}\n'
                f':mMange: xxxxxxxxxxxxxxxxxxxxxx\n')
            return False
        return True

    def __add_docs_cursor_to_list(self) -> int:
        if len(self.db.docs_list) < self.db.clusters_num and not self.__method_stop_add_docs_to_list_condition():
            skipter = (2 * self.db.clusters_num) - len(self.db.docs_list)
            log(f':mManger:log: #### Cluster skipter load [{skipter}]')

            cards_temp_cursor = self.__db.getCurrentDocsByLimit(self.db.db_index, skipter)

            for card in cards_temp_cursor:
                self.db.docs_list.append(card)
                # Index start on [0 <= index < n]
                self.db.db_index += 1
            return skipter
        return 0

    def __endThread(self):
        log(':mManage: ■■■■■■■■ Send End Thread ■■■■■■■■')
        for slave in self.workers:
            self.__stat.history_stat(slave.join())
            log(f':mManage:\t\t - Cluster {slave.name} JOINED')

        for worker in self.workers:
            del worker

        del self.workers

    def __init_time_event(self):
        self.__timer.add('big_loop_report')

    def __find_time(self, lst, key, value):
        for i, dic in enumerate(lst):
            if dic[key] == value:
                return i
        return -1
