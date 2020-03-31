"""
ไปอ่านผลการทดลองใน 630212_exp_alb_count.py
"""
from datetime import datetime
from time import time

import bson

from fbta_browser_worker import FBTADriver
from fbta_configs import FBTAConfigs
from fbta_node_master import FBTANodeMaster
from fbta_settings import FBTASettings
from pymongo import MongoClient

import re as regex

if __name__ == '__main__':
    fb_url_w = 'https://www.facebook.com'

    settings = FBTASettings('fadehara')
    configs = FBTAConfigs()

    settings.kill_driver_on_end = True
    settings.driver_path = r'./Driver/chromedriver_76.exe'
    settings.dir_cookies = r'./cookies/'
    settings.use_nodeMaster_loadCookie = True

    settings.use_nodeMaster = False
    settings.init_node_master_browser = False

    settings.renew_index = False
    settings.fast_worker = True
    settings.date_process = [2017, 10, 1]
    settings.dir_path_detail = settings.DIR_DETAIL_NEW_ALL_RUN
    #
    # node_master = FBTANodeMaster(settings, configs)
    # node_master.start()
    #
    # re = FBTADriver(node_master)
    #
    # re.add_cookie_from_file()
    # re.get('https://m.facebook.com')
    # re.delete_cookie('noscript')
    # re.set_header_chrome()

    db_name = 'fbta_20200202_1816'
    reg_str = '(?<=[\>])(\+[0-9,]+)(?=[\<])'

    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('03_post_page')
    collection_new = db.get_collection('05_album_count')

    key = {'album-next-downloaded': {'$exists': False}, 'dataft.dataft-type': {'$exists': True}}
    docs_post = collection.find(key)
    docs_album = collection_new.find()

    time_all_start = time()

    print(docs_post.count())

    for doc in docs_album:
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

        xxx = ''.join(regex.findall(reg_str, source)).replace('+', '').replace(',','').strip()
        img_c = int(xxx) if xxx else 0
        data['img-count'] = img_c

        if img_c > 999:
            print(data['img-count'], data['download-time'])
        # print(data['source'])
        # collection_new.insert_one(data)
    print('Finised', time() - time_all_start)
