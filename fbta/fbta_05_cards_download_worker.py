import json
import time

import bson

from fbta_global_database_manager import FBTADBManager
from fbta_03_history_download_method import FBTAHistoryDownloaderMethod
from fbta_main_worker import FBTAMainWorker
from fbta_node_master import FBTANodeMaster
from fbta_log import log
from bson.json_util import loads


class FBTACardsDownloadWorker(FBTAMainWorker):
    def __init__(self, node_master: FBTANodeMaster, db: FBTADBManager):
        self.__node_master = node_master
        self.__db = db

        FBTAMainWorker.__init__(self, node_master)
        self.__activity: FBTAHistoryDownloaderMethod = FBTAHistoryDownloaderMethod.NONE

    def after_init(self):
        self.__activity = FBTAHistoryDownloaderMethod(self.__node_master, self.node_worker, self.__db)
        self.__activity.slave_name = self.name

    def slave_method(self, docs):
        # print(f':History_Worker: [{self.name}] Slave method Work on', docs['title'])
        self.__cards_download_method(docs)
        # print(f':History_Worker:\t\t[{self.name}] WORK [{docs["_id"]}] finished [{self.browser.title}]')

    def __cards_download_method(self, docs):
        url = docs.get('main-link')

        if url != '#':
            # Resume System
            if docs.get('next-downloaded') is None:
                self.node_worker.goto_Secure(url)
                log('>>>>', self.name, docs.get('_id'), self.node_worker.browser.driver.title)
                bsref = bson.DBRef(self.__db.current_get_name(), bson.ObjectId( docs.get('_id')), self.__db.get_db_name())
                data = {
                    'history-cluster-id': str(docs.get('history-cluster-id')) + ',' + str(self.name),
                    'url': url,
                    'source': str(self.node_worker.browser.driver.page_source),
                    'refer-id': docs.get('_id'),
                    'timer-download': time.time() - self.process_timer_start,
                    'history': bsref
                }
                self.__db.next_collection_insert_one(data)

            self.stat.add_stat('posts-counter')

        else:
            self.stat.add_stat('posts-broken-links')
