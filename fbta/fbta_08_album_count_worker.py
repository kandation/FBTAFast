import re as regex
import shutil
import time
from datetime import datetime
from typing import List, Optional

from fbta_08_album_count_method import FBTAAlbumCountMethod
from fbta_global_database_manager import FBTADBManager
from fbta_03_history_download_method import FBTAHistoryDownloaderMethod
from fbta_main_worker import FBTAMainWorker
from fbta_node_master import FBTANodeMaster
from fbta_log import log


class FBTAAlbumCountWorker(FBTAMainWorker):
    def __init__(self, node_master: FBTANodeMaster, db: FBTADBManager):
        self.__node_master = node_master
        self.__db = db

        FBTAMainWorker.__init__(self, node_master)
        # self.__activity: FBTAHistoryDownloaderMethod = FBTAHistoryDownloaderMethod.NONE
        self.__photos_method: FBTAAlbumCountMethod = FBTAAlbumCountMethod.NONE

        self.REGX_PATTERN = '(?<=[\>])(\+[0-9]+)(?=[\<])'

    def after_init(self):
        """Read instruction in Lab expr"""
        self.browser.driver.delete_cookie('noscript')
        self.browser.driver.set_header_chrome()

        self.__photos_method = FBTAAlbumCountMethod(self.browser)

    def slave_method(self, docs):
        self.get_album_count(docs)

    def get_album_count(self, doc):
        timer_dl_start = time.time()
        data = {
            'img-count': -1,
            'download-time': -1,
            'url': '',
            'history': doc.get('_id'),
            'source': '',
        }

        main_url = f"https://www.facebook.com{doc.get('url')}"
        self.browser.goto(main_url)

        try:
            data['source'] = self.browser.driver.page_source
            xxx = ''.join(regex.findall(self.REGX_PATTERN, data['source'])).replace('+', '').strip()
            img_c = int(xxx) if xxx else 0
            data['img-count'] = img_c
            data['url'] = doc.get('url')
            data['download-time'] = time.time() - timer_dl_start
        except BaseException as e:
            data['url'] = doc.get('url')
            data['error'] = {
                'time': str(datetime.now()),
                'exce': str(e)
            }

        print(f":ALBUMWorker: {data['img-count']} @{data['download-time']}")
        self.__db.next_collection_insert_one(data)

