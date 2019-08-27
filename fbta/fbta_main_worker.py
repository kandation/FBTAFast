import copy
import json
from threading import Thread
from typing import List, Optional
from abc import ABCMeta, abstractmethod

import pymongo
from selenium.common.exceptions import WebDriverException

from fbta_node_master import FBTANodeMaster
from fbta_node_worker import FBTANodeWorker
from fbta_statistic import FBTAStatistic
from fbta_log import log


class FBTAVariableDownload:
    def __init__(self):
        self.doc = None
        self.__loop_try_agin = 0

        self.__prev_doc = None

    def new_download(self, doc: pymongo.cursor.Cursor):
        log('add new dowload', doc['_id'])
        if self.doc is not None:
            log('############# WARNING ############')
            log('#         DOCS NOT EMPTY         #')
            log('##################################')
            return False
        self.doc = doc
        return True

    def restart_if_thread_die(self):
        if self.__prev_doc is not None:
            self.doc = self.__prev_doc
        self.__prev_doc = None
        if not self.doc and not self.__prev_doc:
            log(':VDownload: Current and prev docs is None')

    def end_download(self):
        self.doc = None

    def get(self):
        doc = copy.deepcopy(self.doc)
        self.__prev_doc = doc
        self.doc = None
        return doc

    @property
    def prev_job_id(self):
        if self.__prev_doc:
            return self.__prev_doc['_id']
        return -1

    def has_download_url(self):
        return bool(self.doc)


class FBTAMainWorker(Thread, metaclass=ABCMeta):
    NONE = None

    def __init__(self, masters: FBTANodeMaster):
        self.__masterNode = masters
        self.__settings = self.__masterNode.settings
        self.__configs = self.__masterNode.configs

        self.__slave_is_end = False
        self.__slave_is_waiting_job = True

        Thread.__init__(self)

        self.__node_worker: FBTANodeWorker = FBTANodeWorker.NONE
        self.download_current = FBTAVariableDownload()

        self.__stat = FBTAStatistic()

        self.__error_fatal = False

        self.__stop_thread = False

        self.is_ready = False

        self.__return = None

        self.sos_signal = False

        self.slave_class_name = ''
        self.__url = self.__masterNode.url

    def url(self, url) -> str:
        return self.__url.getUrlWithMain(url)

    @property
    def stat(self):
        return self.__stat

    @property
    def configs(self):
        return self.__configs

    @property
    def settings(self):
        return self.__settings

    @property
    def node_worker(self) -> FBTANodeWorker:
        return self.__node_worker

    @property
    def browser(self):
        return self.__node_worker.browser

    @property
    def slave_class_name(self):
        return self.__slave_class_name

    @slave_class_name.setter
    def slave_class_name(self, name):
        self.__slave_class_name = name

    @property
    def slave_name(self):
        return self._slave_name

    @slave_name.setter
    def slave_name(self, name):
        self._slave_name = name

    @property
    def isErrorFatal(self):
        return self.__error_fatal

    @isErrorFatal.setter
    def isErrorFatal(self, cond):
        self.__error_fatal = bool(cond)

    @abstractmethod
    def after_init(self):
        pass

    def run(self):
        # TODO DEBUG METHOD IF USE IN PRODUCTION PLASE USE NORMAL
        self.__init_browser_secure()
        self.after_init()
        self.__download()

    def run_main(self):
        while not self.__stop_thread:
            try:
                run_init_browser_result = self.__init_browser_secure()
                if not run_init_browser_result:
                    break

                try:
                    log(':mWorker: Run After Init')
                    self.after_init()
                except:
                    log(f':mWorker:■■■■■■■■■■■■■■■■■■■■■■■■ def after_init() method is ERROR ■■■■■■■■■■■■■■■■■■■■■■■■')
                    self.__stop_thread = True
                    exit()

                self.__download()
            except:
                log(f':mWorker: [{self.name}] Thread Error Auto Restart')
                self.__restart_variable()

    def __init_browser_secure(self) -> bool:
        ret = False
        try_agin = 0
        while True:
            if try_agin > 10:
                break
            try:
                self.__init_browser()
                ret = True
                break
            except:
                log(f':mWorker: [{self.name}] Init Browser Error Try Agin')
                try_agin += 1
        return ret

    def __restart_variable(self):
        self.__slave_is_waiting_job = True
        self.is_ready = False
        self.sos_signal = False
        self.__loop_try_agin = 0

    def restart_browser(self):
        log(f':mWorker: [{self.name}] get Restart Command')
        self.__restart_variable()
        self.__stat.worker_browser_died += 1

        try:
            del self.__node_worker
        except:
            pass

        self.__init_browser_secure()

    def join(self, timeout: Optional[float] = ...) -> str:
        Thread.join(self)
        return self.__return

    def is_waiting_job(self):
        return self.__slave_is_waiting_job

    def add_job(self, card: pymongo.cursor.Cursor):
        if card:
            log(f':mWorker:\t\t>> {self.__slave_class_name} : '
                f'Add Jobs To [{self.name}]'
                f' [{card["_id"]}]')
        else:
            log(f':mWorker: \t\t !!! [{self.name}] Add jobs get None type ')
        self.__slave_is_waiting_job = False
        self.download_current.new_download(card)

    def end_job(self):
        self.__slave_is_end = True

    def is_end(self):
        return self.__is_must_running()

    def manger_send_active_refresh(self):
        """
        when manager look waiting list and dectect this worker
        spend more time it send 'activate' to worker for refresh
        web browser if it has error will kill cluster
        :return:
        """
        log(':mWorker:\t\t ʕつ•ᴥ•ʔつ --- Get Active ---- ʕつ•ᴥ•ʔつ')

    def __download(self):
        log(f':mWorker: [{self.name}] Start Download')
        self.is_ready = True

        while not self.__is_must_running():
            # TODO DONT Forget try-except to protect
            self.__method_normal_worker_run()
            # try:
            #     self.__method_normal_worker_run()
            #     pass
            #
            # except WebDriverException as web_error:
            #     log(f':mWorker: [{self.name}] WEBERROR as [{web_error}]')
            #     self.__init_browser()
            #     self.__stat.worker_browser_died += 1
            #
            # except Exception as e:
            #     log(f':mWorker: ??? [{self.name}] Worker die by Exception [{e}]')
            #
            #
            # except:
            #     log(f'mWorker: ???? [{self.name}] Thread Die by something')
            #     if self.__loop_try_agin > 10:
            #         self.sos_signal = True
            #     else:
            #         self.download_current.restart_if_thread_die()
            #     self.__loop_try_agin += 1

        log(f':mWorker:\t\t>> {self.slave_class_name} [{self.name}] is Out Loop')

        self.__slave_is_end = True
        log(':mWorker:\t\t>> {class_name} {cluster_id} End Download with {works}'.format(
            class_name=self.slave_class_name,
            cluster_id=self.name,
            works=self.__stat.history_couter_success))
        self.__return = self.__stat.get_worker_stat(self.name)

        self.killBrowser()
        self.__stop_thread = True

    def __is_must_running(self):
        return self.__slave_is_end and not self.download_current.has_download_url()

    def __method_normal_worker_run(self):
        if self.download_current.has_download_url():
            self.__slave_is_waiting_job = False

            log(':mWorker: Add to slave method', self.download_current.doc['_id'])

            self.slave_method(self.download_current.get())

            self.download_current.end_download()

            self.__stat.history_couter_success += 1

        else:
            self.__slave_is_waiting_job = True

    @abstractmethod
    def slave_method(self, docs) -> bool:
        pass

    def get_last_job_finshed(self):
        if self.download_current.prev_job_id:
            return self.download_current.prev_job_id
        else:
            return -1

    def get_prev_id(self):
        return self.download_current.prev_job_id

    def killBrowser(self):
        log(f':mWorker: [{self.name}] start KILL Driver')
        try:
            self.__node_worker.browser.killdriver()
        except:
            log(f'mWorker: [{self.name}] Kill driver  Error but no problem')

        try:
            del self.__node_worker
        except:
            log(f':mWorker: [{self.name}] Delete WORKER_BROWSER_ERROR')

    def __exit__(self, exc_type, exc_val, exc_tb):
        log(':mWorker: send "KILL BROWSER" by exit')
        self.killBrowser()

    def __showListJobsNotify(self):
        pass

    def __init_browser(self):
        self.__node_worker = FBTANodeWorker(self.name, self.__masterNode)
        if self.settings.use_nodeSlave:
            self.__node_worker.browser.use_no_script(True)
            self.__node_worker.browser.name = self.name
            self.__node_worker.setFBScope(0)
            self.__node_worker.run()
