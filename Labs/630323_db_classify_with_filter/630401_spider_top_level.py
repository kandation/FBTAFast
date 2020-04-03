import time
from pprint import pprint

from parsel import Selector
from pymongo import MongoClient

from fbta_configs import FBTAConfigs
from fbta_driver import FBTADriver
from fbta_node_master import FBTANodeMaster
from fbta_settings import FBTASettings

import json, os
from pprint import pprint
from typing import List, Optional

from parsel import Selector
from pymongo import MongoClient

import m_630323_01_style as m_style


db_name = 'fbta_20200216_0000'
db_name = 'fbta_20200202_1816'

import collections


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def find12img(url_new):
    res_new = session.get(url_new)
    sel_new = Selector(res_new.text)
    ks = sel_new.css('#thumbnail_area > a')
    more_items = sel_new.css('#m_more_item > a')
    if more_items:
        more_item_link = more_items[0].attrib.get('href')
        print(f'IsMore: {more_item_link}')
    for kps in ks:
        jsp = kps.attrib.get('href')
        print(jsp)


if __name__ == '__main__':
    """
    FBAlbumDownloader Labs Version @620829
    """
    images = []

    fb_url_w = 'https://www.facebook.com'
    fb_url_m = 'https://m.facebook.com'

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

    node_master = FBTANodeMaster(settings, configs)
    node_master.start()

    session = FBTADriver(node_master)

    session.add_cookie_from_file()
    session.get('https://m.facebook.com')
    session.delete_cookie('noscript')
    # session.set_header_chrome()

    headers = {
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
    }
    session.set_headers_custome(headers)

    page_error_topic = ['Content Not Found']

    client = MongoClient()

    db = client.get_database(db_name)
    collection = db.get_collection('05_album_count')
    test_collection = db.get_collection('99_test_rec_top_level')
    collection_post = db.get_collection('03_post_page')

    docs = collection_post.find()

    # db_find_key = {'dataft.dataft-type': {'$exists': True}}
    # docs_post = collection_post.find(db_find_key)

    url_error = []

    ccc = 0
    collect_list = {str(i): 0 for i in range(7)}
    collect_list_gt0 = {str(i): 0 for i in range(7)}

    allow_type = ['a', 'oa', 'pcb']

    start_time = time.time()

    level = 0

    PAT = '/photo.php?'

    session.get('https://m.facebook.com/story.php?story_fbid=2661592027242706&substory_index=14&id=100000695314425')
    print(session.page_source)
    exit()

    for doc in docs:
        m_source = doc.get('source')
        bs = Selector(doc.get('source', ''))
        dataft_list: List[Optional[Selector]] = bs.css("div[data-ft]")

        if len(dataft_list) != 0:
            dataft_str = m_style.find_max_dataft(dataft_list)
            js = json.loads(dataft_str, encoding='utf8')
            top_level = js.get('top_level_post_id')
            mf_key = js.get('mf_story_key')
            original_content = js.get('original_content_id')
            own_id = js.get('content_owner_id_new')
            page_insights = js.get('page_insights')

            if not mf_key and not original_content:
                print(f"{fb_url_m}/{doc.get('url')}")
                print(js)
                print()
                # print(js)
            # if top_level:
            #     session.get(f'{fb_url_m}/{top_level}')
            #     bs = Selector(doc.get('source', ''))
            #     dataft_list: List[Optional[Selector]] = bs.css("div[data-ft]")
            #     print(dataft_list)

