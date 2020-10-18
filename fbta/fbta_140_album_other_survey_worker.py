import re as regex
import shutil
import time
from datetime import datetime
from typing import List, Optional

from parsel import Selector

from fbta.fbta_global_database_manager import FBTADBManager
from fbta.fbta_03_history_download_method import FBTAHistoryDownloaderMethod
from fbta.fbta_main_worker import FBTAMainWorker
from fbta.fbta_node_master import FBTANodeMaster
from fbta.fbta_log import log


class FBTA140AlbumOtherSurveyWorker(FBTAMainWorker):
    def __init__(self, node_master: FBTANodeMaster, db: FBTADBManager):
        self.__node_master = node_master
        self.__db = db

        FBTAMainWorker.__init__(self, node_master)

        self.PHOTO_PATTERN = '\/([0-9]+)\/|\?fbid=([0-9]+)'
        self.url_patt = 'media/set/?set={a_type}.{aid}'
        # self.url_patt = 'media/set/?set={a_type}.{aid}&type=1'

    def after_init(self):
        """Read instruction in Lab expr"""
        self.browser.driver.set_header_firefox()

    def slave_method(self, docs):
        self.single_surway(docs)

    def single_surway(self, doc):
        """
        ยังไม่ทำ is-more ที่เกินกว่าที่เห็บ ตอนนี้ ขก
        :param doc:
        :return:
        """
        timer_dl_start = time.time()
        load_url = doc.get('load-url')

        self.browser.goto(load_url)

        data_insert = {
            'source': self.browser.driver.page_source,
            'time': time.time() - timer_dl_start
        }

        self.__db.raw_collection_next().update_one({'_id': doc.get('_id')}, {'$set': data_insert})
        self.__db.collection_current_downloaded(doc.get('_id'))
