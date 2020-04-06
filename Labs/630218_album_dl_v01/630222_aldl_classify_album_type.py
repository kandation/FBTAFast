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

if __name__ == '__main__':
    fb_url_w = 'https://www.facebook.com'


    """
    เอาจริงๆ เพื่อประสิทธิภาพแล้ว การค้นหาแบบนี้ ค่อนข้างไวที่เดียวเลย แต่ว่า
    """

    db_name = 'fbta_20200202_1816'

    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('03_post_page')
    collection_new = db.get_collection('05_album_count')

    # key = {'album-next-downloaded': {'$exists': False}, 'dataft.dataft-type': {'$exists': True}}
    # docs_post = collection.find(key)
    docs_album = collection_new.find()

    time_all_start = time()

    # print(docs_post.count())

    REG_PAT_A = '[^o]a\.[0-9]{14,}'
    REG_PAT_OA = 'oa\.[0-9]{14,}'
    REG_PAT_PCB = 'pcb\.[0-9]{14,}'

    index_test = 0

    for doc in docs_album:
        if index_test > 99999999:
            break
        timer_dl_start = time()

        source = doc.get('source')

        data = {
            'img-count': -1,
            'download-time': -1,
            'url': '',
            'history': doc.get('_id'),
            'source': '',
        }

        # print(f"{fb_url_w}{doc.get('url')}")
        # main_url = f"{fb_url_w}{doc.get('url')}"
        # re.get(main_url)



        find_list_check = {
            'a': [],
            'oa': [],
            'pcb': []
        }
        sr_pcb = regex.findall(REG_PAT_PCB, source)
        sr_a = regex.findall(REG_PAT_A, source)
        sr_oa = regex.findall(REG_PAT_OA, source)
        if sr_pcb:
            find_list_check['pcb'] = sr_pcb
        if sr_a:
            find_list_check['a'] = sr_a
        if sr_oa:
            find_list_check['oa'] = sr_oa

        bool_lock_fls = False
        sum_list_len = 0
        for fls_key in find_list_check:
            size_of_list = len(find_list_check[fls_key])
            sum_list_len += size_of_list
            if size_of_list > 0:
                if bool_lock_fls:
                    pass
                    # print(f'{doc.get("img-count")} https://www.facebook.com{doc.get("url")}')
                    # print(find_list_check)
                bool_lock_fls = True

        if sum_list_len <= 0:
            sel = Selector(source)
            text_title = sel.css('title')[0].get()
            print(f'{doc.get("img-count")} ------- https://www.facebook.com{doc.get("url")}')
            print(text_title)
            speed_of_find = time()
            str(source).find('Sorry, this content')
            speed_of_find = time() - speed_of_find

            speed_of_in = time()
            # ใน  firefox mobile จะมี title= Content Not Found
            bool_is_in = "Sorry, this content" in source
            speed_of_in = time() - speed_of_in
            print(f'FindTime = {speed_of_find} vs In = {speed_of_in}')
            if bool_is_in:
                """
                Content Not avalable บางที่ ก็ไม่ถูกเสมอไป เพราะ เจ้าของอาจจะไม่โดนแบนแล้ว
                """
                print('CONTENT NOT AVALIBLE')
            # print(doc['source'])
            # exit()


        xxx = ''.join(sr_pcb).replace('+', '').replace(',', '').strip()
        # img_c = int(xxx) if xxx else 0
        # data['img-count'] = img_c

        # if img_c > 999:
        #     print(data['img-count'], data['download-time'])
        # print(data['source'])
        # collection_new.insert_one(data)
        index_test += 1

    print('Finised', time() - time_all_start)
