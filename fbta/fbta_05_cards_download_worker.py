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
    def __init__(self, node_master: FBTANodeMaster, db: FBTADBManager, *args):
        self.__node_master = node_master
        self.__db = db

        FBTAMainWorker.__init__(self, node_master)
        self.__activity: FBTAHistoryDownloaderMethod = FBTAHistoryDownloaderMethod.NONE

        self.__is_chrome_header = args[0].get('chrome_header', False) if args else False

    def after_init(self):
        if self.__is_chrome_header:
            # ต้องการเก็บ story Version ใหม่
            self.browser.driver.delete_cookie('noscript')
            self.browser.driver.set_header_chrome()

    def slave_method(self, docs):
        if not self.__is_chrome_header:
            self.__cards_download_method(docs)
        else:
            self.__cards_download_chrome_method(docs)

    def __cards_download_method(self, docs):
        url = docs.get('main-link')

        if url != '#':
            # Resume System
            self.node_worker.goto_Secure(url)
            log('>>>>', self.name, docs.get('_id'), self.node_worker.browser.driver.title)
            bsref = bson.DBRef(self.__db.current_get_name(), bson.ObjectId(docs.get('_id')),
                               self.__db.get_db_name())

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

        self.__db.collection_current_downloaded(docs.get('_id'))

    def __cards_download_chrome_method(self, docs):
        # Docs from '98_album_no_duplicate'
        ref: bson.DBRef
        ref = docs.get('ref', [None]).pop(0)
        if ref:
            # Get ref to '03_post_page'
            photo_docs = self.__db.raw_db().dereference(ref)
            print('--------------', photo_docs)

            # ไปยัง Story url เดิมกับครั้งแรก
            url = photo_docs.get('url')
            self.node_worker.goto_Secure(url)

            data = {
                'album-count': {
                    'url': url,
                    'album-count-source': str(self.node_worker.browser.driver.page_source),
                    # TODO: 630410 ว่างๆก็ลบออกด้วย แต่ยังไม่ได้ตรวจสอบ (วนซ้ำฐานข้อมูลเดิม)
                    'ref': bson.DBRef(self.__db.raw_collection_current().name, docs.get('_id'), self.__db.raw_db().name)
                }
            }
            # บนทึกที่เดิมแหละจะได้ใช้ง่ายๆ
            self.__db.raw_collection_current().update_one({'_id': docs.get('_id')}, {'$set': data})
        # self.__db.collection_current_downloaded(photo_docs.get('_id'))
