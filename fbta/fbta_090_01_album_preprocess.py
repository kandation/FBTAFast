"""
# COUNTING_AND_CREATE_URL_FOR_NEXT_PAGE_ALBUM
# Pre-process from LOAD_NEW_STORY_WITH_CHROME_HEADER
"""

from datetime import datetime
from pprint import pprint
from time import time
import re as regex

from bson import DBRef
from parsel import Selector

from pymongo import MongoClient

from fbta.fbta_log import log

from fbta.fbta_100_00_create_photo_from_album import get_photo_fbid


class FBTA0901MoreAlbumPreProcess():
    def __init__(self):
        """  """
        pass

    def find12img(self, source):
        data_ret = {
            'is-more': '',
            'photos': [],
        }

        sel_new = Selector(source)
        ks = sel_new.css('#thumbnail_area > a')
        more_items = sel_new.css('#m_more_item > a')

        if more_items:
            more_item_link = more_items[0].attrib.get('href')
            data_ret['is-more'] = more_item_link

        for kps in ks:
            jsp = kps.attrib.get('href')
            data_ret['photos'].append(jsp)

        return data_ret

    def main(self, db_name):
        """
        Ignore case ไม่ได้ถูกประมวลผลอยู่แล้ว เลยไม่จำเป็นต้องมีตัวกรอง
        """
        client = MongoClient()
        db = client.get_database(db_name)
        collection = db.get_collection('98_album_no_duplicate')

        key = {}
        docs_post = collection.find(key)

        time_all_start = time()
        log(f':MORE_ALBUM: Docs in collection = {collection.count_documents(key)}')

        for doc in docs_post:
            cluster = doc.get('photo-cluster')
            source = cluster.get('source')

            px = self.find12img(source)
            cluster.update(px)

            collection.update({'_id': doc.get('_id')}, {'$set': doc})

        print('Finished', time() - time_all_start)

#
# if __name__ == '__main__':
#     nno = FBTA0901MoreAlbumPreProcess()
#     nno.main('fbta_20200422_0329')
