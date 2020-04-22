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

from fbta_log import log

from fbta_100_00_create_photo_from_album import get_photo_fbid


class FBTA150MoreAlbumPreProcess():
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
        collection = db.get_collection('aa_album_url')
        coll_photo_tank = db.get_collection('99_photos_tank')

        key = {}
        docs_post = collection.find(key)

        time_all_start = time()
        log(f':MORE_ALBUM: Docs in collection = {collection.count_documents(key)}')

        for doc in docs_post:
            source = doc.get('source')
            is_end = doc.get('is-end')
            ref_album = doc.get('ref')

            refobj = db.dereference(ref_album)
            aid = refobj.get('aid')
            px = self.find12img(source)

            ref_new_album_url = DBRef(collection.name, doc.get('_id'), db.name)

            # When Album has update this line is active
            if is_end and px['is-more'] != '':
                px['re-index'] = True

            data = {'detail': px}
            collection.update({'_id': doc.get('_id')}, {'$set': data})

            # Step 02 : Add photo url to photo_tank
            for photo_url in px['photos']:
                photo_fbid = get_photo_fbid(photo_url)
                photo_tank_data = {}
                photo_tank_data['photo-id'] = photo_fbid
                photo_tank_data['aid'] = aid
                photo_tank_data['type'] = 'album2photo'
                photo_tank_data['url'] = photo_url
                photo_tank_data['refs'] = {}
                photo_tank_data['refs']['more'] = ref_new_album_url
                photo_tank_data['refs']['album'] = ref_album

                print(photo_tank_data)
                coll_photo_tank.insert_one(photo_tank_data)

        print('Finished', time() - time_all_start)


if __name__ == '__main__':
    nno = FBTA150MoreAlbumPreProcess()
    nno.main('fbta_20200422_0329')
