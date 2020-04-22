"""
ไปอ่านผลการทดลองใน 630212_exp_alb_count.py
"""
import json
from datetime import datetime
from pprint import pprint
from time import time
from urllib.parse import unquote

import bson
from bson import DBRef
from parsel import Selector

from fbta_browser_worker import FBTADriver
from fbta_configs import FBTAConfigs
from fbta_node_master import FBTANodeMaster
from fbta_settings import FBTASettings
from pymongo import MongoClient

import re as regex


def splitter_url(url, counter, start_img_num):
    """ แบ่ง URL จากรูปภาพเริ่มต้น"""
    url_list = []
    counter += start_img_num

    num_rem = counter % 12
    num_url = (counter // 12) if num_rem <= 0 else (counter // 12) + 1

    for c in range(1, num_url):
        load_url = f'{url}&s={12 * c}&refid=56'
        is_end = c == num_url - 1
        d = {
            'url-id': c,
            'load-url': load_url,
            'is-end': is_end
        }
        url_list.append(d)
    return url_list


if __name__ == '__main__':
    fb_url_w = 'https://www.facebook.com'

    db_name = 'fbta_20200417_0125'
    # db_name = 'fbta_20200412_1345'
    reg_str = '(?<=[\>])(\+[0-9,]+)(?=[\<])'

    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('98_album_no_duplicate')
    coll_more = db.get_collection('AA_album_no_duplicate')
    # collection_new = db.get_collection('98_0_album_sv')

    key = {'photo-cluster.0.is-more': {'$ne': ''}}
    docs_post = collection.find(key)
    # docs_album = collection_new.find()

    time_all_start = time()

    print(docs_post.count())

    for doc in docs_post:
        album_counter = doc.get('alum-count')
        timer_dl_start = time()

        data = {

            'img-count': -1,
            'img-count-start': 0,
            'split-url': [],

        }

        if album_counter:
            source = album_counter.get('album-count-source')
            oid = doc.get('_id')
            first_ref = doc.get('ref')[0]

            str_more_img = ''.join(regex.findall(reg_str, source)).replace('+', '').replace(',', '').strip()

            # Call Ref_ALBUM cause need START_IMG_NUM in story
            ref_album_duplicate = first_ref
            ref_album_dup_obj = db.dereference(ref_album_duplicate)

            # get START_IMG_NUM from exist key (in Collection)
            old_img_tag = ref_album_dup_obj['description']['album']['data-album']['album-cluster']['img']
            num_old_img = sum([len(old_img_tag[key_cx]) for key_cx in old_img_tag])
            data['img-count-start'] = num_old_img

            # ref_for_more_album = DBRef(collection.name, oid, db.name)
            # data['history'] = ref_for_more_album

            if str_more_img:
                urlx = doc.get('photo-cluster')[0].get('url')
                ls = splitter_url(urlx, int(str_more_img), num_old_img)

                data['split-url'] = ls
                data['img-count'] = int(str_more_img)

                # ออกจากลูปแก้ไขข้อมูลใหม่
                # break

            else:
                """
                อาจจะเกิดจากความผิดพลาด ตอน Restart browser
                """
                data['error'] = {'code': 'browser-restart'}

            data = {'album-count': data}
            collection.update({'_id': oid}, {'$set': data})

        print(data)

        # ref_album_duplicate = doc.get('ref')[0]
        #
        # # print(pxz)
        # # print(source)
        # ref_album_dup_obj = db.dereference(ref_album_duplicate)
        # # ref_album_dup_obj['source'] = ''
        # with open('gg.html', mode='w') as fo:
        #     fo.write(ref_album_dup_obj['source'])
        # exit()

        # pprint(ref_album_dup_obj['source'])

    print('Finised', time() - time_all_start)
