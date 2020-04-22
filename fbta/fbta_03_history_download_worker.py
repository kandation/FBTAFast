from fbta_global_database_manager import FBTADBManager
from fbta_03_history_download_method import FBTAHistoryDownloaderMethod
from fbta_main_worker import FBTAMainWorker
from fbta_node_master import FBTANodeMaster
from fbta_log import log


class FBTAHistoryDownloadWorker(FBTAMainWorker):
    def __init__(self, node_master: FBTANodeMaster, db: FBTADBManager):
        self.__node_master = node_master
        self.__db = db

        FBTAMainWorker.__init__(self, node_master)
        self.__activity: FBTAHistoryDownloaderMethod = FBTAHistoryDownloaderMethod.NONE

    def after_init(self):
        self.__activity = FBTAHistoryDownloaderMethod(self.__node_master, self.node_worker, self.__db)
        self.__activity.slave_name = self.name

    def slave_method(self, docs):
        print(f':History_Worker: [{self.name}] Slave method Work on', docs['title'])
        self.__activity_download(docs['url'], docs.get('_id'))
        print(f':History_Worker:\t\t[{self.name}] WORK [{docs["_id"]}] finished [{self.browser.title}]')

    def __activity_download(self, url, doc_id):
        self.node_worker.goto_Secure(url)
        pageCounter = 0
        while True:
            print(f':History_Worker: {self.name} isFound Timeline={self.__activity.hasTimeline()}')
            if self.__activity.hasTimeline():
                if self.__activity.getPage_NextMoreLoad(True, self.name):
                    self.__activity.addPageToDb(doc_id)
                    # ss = self.node_worker.screenshot_fullpage(self.__activity.page['title'],
                    #                                           self.configs.dir_seq_01_Activity)
                    # if ss:
                    #     self.stat.add_stat('hdw_screenshot_success')
                    # else:
                    #     self.stat.add_stat('hdw_screenshot_fail')
                    # self.stat.add_stat('hdw_couter_page')
                else:
                    __current_url = self.__activity.page.get('current-url')
                    __next_url = self.__activity.page.get('next-url')
                    log(f':History_Worker: Ended on Current_url: {__current_url} Next_url {__next_url}')
                    break

            else:
                log(f':History_Worker: \t>[{self.name}] Stop MonthMoreLoad with [{pageCounter}] pages [Finished]')
                break

            if self.__activity.checkIsShouldGoing():
                self.node_worker.goto_Secure(self.__activity.getNextUrl())
            else:
                log(f':History_Worker: ✖✖✖ [{self.name}] Break Because time least than settings')
                self.__db.collection_current_downloaded(doc_id)
                break
