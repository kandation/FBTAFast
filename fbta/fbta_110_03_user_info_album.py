"""

"""
import unittest
from datetime import datetime
from time import time
import re as regex
from urllib.parse import parse_qs

from pymongo import MongoClient

from fbta.fbta_log import log


class FBTA11001UserInfoAlbum:
    def __init__(self):
        """ Find user-info from url in URL_PHOTO_TANK """
        pass

    def get_user_info(self, url):
        urls = str(url).split('/')

        user_info = {'user-info': {}}
        PATT_GROUPS = '\/groups\/(.+)\?'

        if 'groups/' in url:

            key_user = regex.match(PATT_GROUPS, url)
            gruop_id = ''.join(key_user.groups())


            user_info['user-info']['info'] = gruop_id
            user_info['user-info']['type'] = 'gid'

        else:
            url_parse = parse_qs(urls[1])

            if url_parse:
                user_info['user-info']['info'] = url_parse.get('id', '')[0]
                user_info['user-info']['type'] = 'id'
            else:
                user_info['user-info']['info'] = urls[1]
                user_info['user-info']['type'] = 'user'

        return user_info

    def main(self, db_name, ignore_list=None):

        client = MongoClient()
        db = client.get_database(db_name)
        collection = db.get_collection('98_album_no_duplicate')

        docs_post = collection.find()
        time_all_start = time()

        log(f':PHOTO_TANK_IGNORE: Docs in collection = {collection.estimated_document_count()}')

        for doc in docs_post:
            try:
                gx = doc.get('photo-cluster').get('photos')[0]
            except:
                print(doc.get('photo-cluster').get('url'))
            user_info = self.get_user_info(gx)
            user_current = user_info['user-info']['info']
            if ignore_list and user_current in ignore_list:
                user_info['user-info']['ignore'] = True

            print(user_info)
            collection.update({'_id': doc.get('_id')}, {'$set': user_info})

        print('Finished', time() - time_all_start)


if __name__ == '__main__':
    """
    TODO: 630423 - แก้ปัญหา https://m.facebook.com/media/set/?set=pcb.745428045950253 with firefox โดนรีพอทว่าสแปมด้วย
    """


    nno = FBTA11001UserInfoAlbum()
    nno.main('fbta_20200423_0244', [])
