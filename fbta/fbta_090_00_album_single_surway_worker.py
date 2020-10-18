import re as regex
import shutil
import time
from datetime import datetime
from typing import List, Optional

from parsel import Selector

from fbta_global_database_manager import FBTADBManager
from fbta_03_history_download_method import FBTAHistoryDownloaderMethod
from fbta_main_worker import FBTAMainWorker
from fbta_node_master import FBTANodeMaster
from fbta_log import log


class FBTA090AlbumSingSurveyWorker(FBTAMainWorker):
    def __init__(self, node_master: FBTANodeMaster, db: FBTADBManager):
        self.__node_master = node_master
        self.__db = db

        FBTAMainWorker.__init__(self, node_master)

        self.PHOTO_PATTERN = '\/([0-9]+)\/|\?fbid=([0-9]+)'
        self.url_patt = 'media/set/?set={a_type}.{aid}'
        self.url_patt_album = '{aid}'
        # self.url_patt = 'media/set/?set={a_type}.{aid}&type=1'

    def after_init(self):
        """Read instruction in Lab expr"""
        self.browser.driver.set_header_firefox()

    def slave_method(self, docs):
        self.single_surway(docs)

    def find12img(self, url_new):
        data_ret = {
            'url': str(url_new),
            'source': '',
            'is-more': '',
            'photos': []
        }
        self.browser.goto(url_new)
        sel_new = Selector(self.browser.driver.page_source)
        data_ret['source'] = self.browser.driver.page_source
        ks = sel_new.css('#thumbnail_area > a')
        more_items = sel_new.css('#m_more_item > a')

        if more_items:
            more_item_link = more_items[0].attrib.get('href')
            data_ret['is-more'] = more_item_link

        for kps in ks:
            jsp = kps.attrib.get('href')
            data_ret['photos'].append(jsp)

        return data_ret

    def single_surway(self, doc):
        timer_dl_start = time.time()
        fb_url_m = 'https://m.facebook.com/'
        a_type = doc.get('type')
        aid = doc.get('aid')

        user_patt_switch = self.url_patt_album if a_type == 'a' else self.url_patt

        url = fb_url_m + user_patt_switch.format(a_type=a_type, aid=aid)

        data_insert = {'photo-cluster': [self.find12img(url)], 'download-time': time.time() - timer_dl_start}

        print(f":AlbumSGSWorker: Get Album Photos Single {aid} @{data_insert['download-time']}")
        self.__db.raw_collection_next().update_one({'_id': doc.get('_id')}, {'$set': data_insert})
        self.__db.collection_current_downloaded(doc.get('_id'))
