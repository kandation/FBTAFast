"""
ค้าหาชื่อ
"""
import json
import urllib
from datetime import datetime
from time import time
from urllib.parse import unquote, parse_qs

import bson
from bson import DBRef
from parsel import Selector

from fbta_browser_worker import FBTADriver
from fbta_configs import FBTAConfigs
from fbta_node_master import FBTANodeMaster
from fbta_settings import FBTASettings
from pymongo import MongoClient

import re as regex


def get_user_info(url):
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


if __name__ == '__main__':
    fb_url_w = 'https://www.facebook.com'

    db_name = 'fbta_20200412_1345'
    reg_str = '(?<=[\>])(\+[0-9,]+)(?=[\<])'

    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('99_photos_tank')
    coll_more = db.get_collection('AA_album_no_duplicate')
    # collection_new = db.get_collection('98_0_album_sv')

    # key = {'photo-cluster.0.is-more': {'$ne': ''}}
    docs_post = collection.find()
    # docs_album = collection_new.find()

    time_all_start = time()

    print(docs_post.count())

    for doc in docs_post:
        url = doc.get('url')
        urls = str(url).split('/')

        user_info = {'user-info': {}}
        url_parse = urllib.parse.parse_qs(urls[1])

        if url_parse:
            user_info['user-info']['info'] = url_parse.get('id', '')[0]
            user_info['user-info']['type'] = 'id'

        else:
            user_info['user-info']['info'] = urls[1]
            user_info['user-info']['type'] = 'user'

        print(user_info)

        if '100000695314425' == user_info['user-info']['info']:
            print(url)
            exit()
