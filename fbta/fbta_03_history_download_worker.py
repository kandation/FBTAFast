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
        self.__activity = FBTAHistoryDownloaderMethod(self.__node_master, self.worker_browser, self.__db)
        self.__activity.slave_name = self.name

    def slave_method(self, docs):
        print(f':History_Worker: [{self.name}] Slave method Work on', docs['title'])
        self.__activity_download(docs['url'])
        print(f':History_Worker:\t\t[{self.name}] WORK [{docs["_id"]}] finished [{self.browser.title}]')

    def __activity_download(self, url):
        self.worker_browser.goto_Secure(url)
        pageCounter = 0
        while True:
            print(self.name, self.__activity.hasTimeline())
            if self.__activity.hasTimeline():
                if self.__activity.getPage_NextMoreLoad(True, self.name):
                    self.__activity.addPageToDb()
                    ss = self.worker_browser.screenshot_fullpage(self.__activity.page['title'], self.configs.dir_seq_01_Activity)
                    if ss:
                        self.stat.add_stat('hdw_screenshot_success')
                    else:
                        self.stat.add_stat('hdw_screenshot_fail')
                    self.stat.add_stat('hdw_couter_page')
                else:
                    print(':HDW-DEBUG:',self.__activity.page)
                    break

            else:
                log(f':History_Worker: \t>[{self.name}] Stop MonthMoreLoad with [{pageCounter}] pages [Finished]')
                break

            if self.__activity.checkIsShouldGoing():
                self.worker_browser.goto_Secure(self.__activity.getNextUrl())
            else:
                log(f':History_Worker: ✖✖✖ [{self.name}] Break Because time least than settings')
                break
