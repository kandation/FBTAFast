"""
    Survey Fb_id with username for ignore list
    Warning : More request concern the most people will be banned by facebook
"""

import time
from urllib.parse import parse_qs, urlparse
from pprint import pprint

from parsel import Selector
from pymongo import MongoClient

import re as regex

from fbta_configs import FBTAConfigs
from fbta_driver import FBTADriver
from fbta_node_master import FBTANodeMaster
from fbta_settings import FBTASettings

import json, os
from pprint import pprint
from typing import List, Optional

from parsel import Selector
from pymongo import MongoClient

db_name = 'fbta_20200412_1345'


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
    """
    FIND FACEBOOK ID BY NAME
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

    # node_master = FBTANodeMaster(settings, configs)
    # node_master.start()
    #
    # session = FBTADriver(node_master)
    #
    # session.add_cookie_from_file()
    # session.get('https://m.facebook.com')
    # session.delete_cookie('noscript')
    # # session.set_header_chrome()
    #
    # headers = {
    #     # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
    # }
    # session.set_headers_custome(headers)
    #
    # page_error_topic = ['Content Not Found']

    client = MongoClient()

    db = client.get_database(db_name)
    collection = db.get_collection('99_photos_tank')
    coll_test = db.get_collection('xx_test_630419')

    docs = collection.find()

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

    users = set()

    urz = 'https://m.facebook.com/Chanins-Workshop-214903195669536'

    # session.get(urz)
    # source = session.page_source
    # sel = Selector(source)
    # pza = sel.xpath("//a[contains(@href,'about.php?')]")
    # print(pza)

    patt = '^[0-9]*$'
    for doc in docs:
        gx = doc.get('url')
        pz = get_user_info(gx)
        zz = pz['user-info']['info']
        users.add(pz['user-info']['info'])
        if pz['user-info']['type'] == 'gid':
            print(pz)
    exit()

    print(len(users))
    exit()
    #
    # for user in users:
    #     info = ''
    #     url = f"{fb_url_m}/{user}"
    #     session.get(url)
    #     source = session.page_source
    #
    #     url_ps = urlparse(session.current_url)
    #
    #     data = {
    #         'url': url,
    #         'url-new': session.current_url,
    #         'source': source
    #     }

        # coll_test.insert_one(data)

        # print(url_ps, url_ps.path)
        #
        # x = regex.search(patt, user)
        # if x:
        #     """USER ID IS NUMBER"""
        #     if '/profile.php' in session.current_url:
        #         info = user
        #     else:
        #         info = url_ps.path[1:]
        # else:
        #     """User id is string"""
        #     sel = Selector(source)
        #     pza = sel.xpath("//a[contains(@href,'about')]")
        #     pzm = sel.xpath("//a[contains(@href,'more')]")
        #     href = pzm.attrib.get('href')
        #
        #     if href:
        #         if 'pages' in href:
        #             pid = str(href).split('/')[3]
        #             print(pid)
        #         else:
        #             print(href)
        #     else:
        #         print(f':PAGE_ERROR: {user}')
        # print()

        # sel = Selector(source)
#
