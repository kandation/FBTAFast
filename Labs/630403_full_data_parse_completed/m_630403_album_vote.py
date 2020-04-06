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
    m_source = '+'.join(source)
    for key_pat in patterns:
        temp = regex.findall(patterns.get(key_pat), m_source)
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


def find_album_id(data_pp, type_pp):
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

    data_for_insert = {'data-album':
        {
            'album-type': type_pp,
            'album-cluster': {'type': 'n/a', 'img': {}},
            'album-id': 'n/a'
        }
    }

    # สร้าง Dict สำหรับ PATTERN
    find_list_check = generate_empty_of_regex(REGEX_PATTERNS)

    # เพิ่ม PATTERN ที่เจอเข้าไปยัง LIST ของ {'a':[],...}
    find_type_of_album(find_list_check, REGEX_PATTERNS, data_pp)

    """
    ที่ยังเก็บโค๊ตนี้ไว้เพื่อเป็น secure function ที่มาช่วยรับประกันว่าในอนาคตถ้ามีเหตุแปลกกว่านี้ สามารถสลับใช้โค๊ตนี้ทำงานได้เลย
    """
    # ค้นหาว่า LIST ไหนว่างบ้าง ถ้าว่างให้เป็น False
    bool_duplicate_patterns = [len(find_list_check.get(x)) > 0 for x in find_list_check]
    # หับจำนวน หัวข้อใดบ้างที่ ไม่ว่าง เพื่อแยกประเภท
    sum_bool_duplicate_patterns = sum(bool_duplicate_patterns)

    type_album = 'n/a'

    if sum_bool_duplicate_patterns == 0:
        # ไม่มีทางเกิดขึ้นเพราะ pre-process มาแล้ว
        type_album = 'video/maybe'

    elif sum_bool_duplicate_patterns == 1:
        # เกิดขึ้นกรณีเดียว เพราะ ไม่มีทางที่จะมี album-id 2อันเกิดขึ้นในโพสเดียว
        type_album = find_possible_type(find_list_check, bool_duplicate_patterns)

    data_for_insert['data-album']['album-cluster']['type'] = type_album

    # ทุกอย่างที่ไม่ใช่วีดีโอ ให้หา album_id
    if sum_bool_duplicate_patterns > 0:
        album_id = find_possible_album_id(find_list_check[type_album])
        data_for_insert['data-album']['album-cluster']['img'] = find_list_check
        data_for_insert['data-album']['album-id'] = album_id

    return data_for_insert
