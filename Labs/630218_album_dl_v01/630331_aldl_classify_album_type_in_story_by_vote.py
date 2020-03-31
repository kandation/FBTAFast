from datetime import datetime
from time import time

import bson
from parsel import Selector

from fbta_browser_worker import FBTADriver
from fbta_configs import FBTAConfigs
from fbta_node_master import FBTANodeMaster
from fbta_settings import FBTASettings
from pymongo import MongoClient

import re as regex


def generate_empty_of_regex(patterns):
    return {str(key_pat): [] for key_pat in patterns}


def find_type_of_album(check_list: dict, patterns: dict, source: str):
    """ ถ้ามีการหาตาม pattern เจอ จะทำการเพิ่มไปใน list """
    for key_pat in patterns:
        temp = regex.findall(patterns.get(key_pat), source)
        if temp:
            check_list[key_pat] = temp


def find_possible_type(finder: dict, finder_size: list) -> str:
    # ใช้ max เพราะ ไม่แน่ใจว่าบางที่ อาจจะมีพวกที่หลุดมาก็ได้ จะได้ไม่ถูกไปกองที่ index 0
    index = finder_size.index(max(finder_size))
    key_album = list(finder.keys())[index]
    return key_album


def find_possible_album_id(posible_type: list):
    REG_PAT_NUMBER = '[0-9]+'
    str_possible = '+'.join(posible_type)
    k = regex.findall(REG_PAT_NUMBER, str_possible)

    # หาว่าอัลบัมหลักคืออะไร (ส่วนใหญ่ก็มีแค่ 1 เท่านั้นแหละ)
    # เชื่อมั่นว่า input จะเป็น album type ที่แท้จริง ไม่ใช่ link ของ post
    album_id_from_vote = max((k.count(x), x) for x in set(k))[1]
    return album_id_from_vote

i=0
if __name__ == '__main__':
    fb_url_w = 'https://m.facebook.com'

    """
    เอาจริงๆ เพื่อประสิทธิภาพแล้ว การค้นหาแบบนี้ ค่อนข้างไวที่เดียวเลย แต่ว่า
    
    ::สมบูรณ์แล้ว 630331
    """
    lsn = {}

    db_name = 'fbta_20200202_1816'
    # db_name = 'fbta_20200331_0107'

    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('03_post_page')

    key = {'dataft.dataft-type': {'$exists': True}}
    docs_album = collection.find(key)

    REG_PAT_A = '[^o]a\.[0-9]{13,}'
    REG_PAT_OA = 'oa\.[0-9]{13,}'
    REG_PAT_PCB = 'pcb\.[0-9]{13,}'
    REG_PAT_GM = 'gm\.[0-9]{13,}'

    REGEX_PATTERNS = {
        'a': REG_PAT_A,
        'oa': REG_PAT_OA,
        'pcb': REG_PAT_PCB,
        'gm': REG_PAT_GM
    }

    for doc in docs_album:
        data_for_insert = {'data-album':
            {
                'album-type': doc.get('dataft').get('dataft-type'),
                'album-cluster': {'type': 'n/a', 'img': {}},
                'album-id': 'n/a'
            }
        }

        page_source = doc.get('source')

        # สร้าง Dict สำหรับ PATTERN
        find_list_check = generate_empty_of_regex(REGEX_PATTERNS)

        # เพิ่ม PATTERN ที่เจอเข้าไปยัง LIST ของ {'a':[],...}
        find_type_of_album(find_list_check, REGEX_PATTERNS, page_source)

        # ค้นหาว่า LIST ไหนว่างบ้าง ถ้าว่างให้เป็น False
        bool_duplicate_patterns = [len(find_list_check.get(x)) > 0 for x in find_list_check]
        # หับจำนวน หัวข้อใดบ้างที่ ไม่ว่าง เพื่อแยกประเภท
        sum_bool_duplicate_patterns = sum(bool_duplicate_patterns)

        type_album = 'n/a'
        album_id = 'n/a'

        if sum_bool_duplicate_patterns == 0:
            type_album = 'video/maybe'
            print(find_list_check)
            # สว่นมากจะเป็นวีดีโอ แต่บางที่ก็อาจจะเป็นเพราะผู้ใช้ถูกลบก็ได้
            # แต่ถ้าจะให้ทำอะไรก็คงเว้นวางไว้รอวิธีการดูดวีดีโอ เพราะวีดีโอจากนี่ คุณภาพต่ำมาก
            print(fb_url_w+doc.get('url'))
            sel = Selector(page_source)
            print(page_source)
            img_video = sel.css('img[alt*="video"]')
            print(img_video)

        elif sum_bool_duplicate_patterns == 1:
            type_album = find_possible_type(find_list_check, bool_duplicate_patterns)

        else:
            sel = Selector(page_source)
            img_section = sel.css('#m_story_permalink_view').css('a > img').xpath('..')
            str_img_section = ''.join(img_section.getall())

            find_list_check = generate_empty_of_regex(REGEX_PATTERNS)
            find_type_of_album(find_list_check, REGEX_PATTERNS, str_img_section)

            bool_duplicate_patterns = [len(find_list_check.get(x)) > 0 for x in find_list_check]
            type_album = find_possible_type(find_list_check, bool_duplicate_patterns)

        data_for_insert['data-album']['album-cluster']['type'] = type_album

        # ทุกอย่างที่ไม่ใช่วีดีโอ ให้หา album_id
        if sum_bool_duplicate_patterns > 0:
            album_id = find_possible_album_id(find_list_check[type_album])
            data_for_insert['data-album']['album-cluster']['img'] = find_list_check
            data_for_insert['data-album']['album-id'] = album_id
            if str(album_id) in lsn:
                lsn[str(album_id)] += 1
            else:
                lsn[str(album_id)] = 1


        # collection.update_one({'_id': doc.get('_id')}, {'$set': data_for_insert})


    for s in lsn:
        if lsn[s] > 1:
            print(lsn[s],':',s)

    print(i)
