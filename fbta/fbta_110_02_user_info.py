"""

"""
import unittest
from datetime import datetime
from time import time
import re as regex
from urllib.parse import parse_qs

from pymongo import MongoClient

from fbta_log import log


class FBTA11001UserInfo:
    def __init__(self):
        """ Find user-info from url in URL_PHOTO_TANK """
        pass

    def get_user_info(self, url):
        urls = str(url).split('/')

        user_info = {'user-info': {}}

        if 'groups' in urls:
            url_parse = parse_qs(urls[2])
            gruop_id = str(url_parse).split('?')[0]
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
        collection = db.get_collection('99_photos_tank')

        docs_post = collection.find()
        time_all_start = time()

        log(f':PHOTO_TANK_IGNORE: Docs in collection = {collection.estimated_document_count()}')

        for doc in docs_post:
            gx = doc.get('url')
            user_info = self.get_user_info(gx)
            user_current = user_info['user-info']['info']
            if ignore_list and user_current in ignore_list:
                user_info['user-info']['ignore'] = True

            collection.update({'_id': doc.get('_id')}, {'$set': user_info})

        print('Finished', time() - time_all_start)
