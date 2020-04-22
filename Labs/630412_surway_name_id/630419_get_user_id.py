"""
ค้าหาชื่อ
"""
import json
import urllib
from datetime import datetime
from time import time
from urllib.parse import unquote, urlparse

import bson
from bson import DBRef
from parsel import Selector

from fbta_browser_worker import FBTADriver
from fbta_configs import FBTAConfigs
from fbta_node_master import FBTANodeMaster
from fbta_settings import FBTASettings
from pymongo import MongoClient

import re as regex

if __name__ == '__main__':
    fb_url_w = 'https://www.facebook.com'

    db_name = 'fbta_20200412_1345'
    reg_str = '(?<=[\>])(\+[0-9,]+)(?=[\<])'

    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('xx_test_630419')
    docs_post = collection.find()

    time_all_start = time()

    print(docs_post.count())
    patt = '^[0-9]*$'
    for doc in docs_post:
        url = doc.get('url')
        url2 = doc.get('url-new')
        source = doc.get('source')

        user = str(url).split('/')[-1]

        url_ps = urlparse(url2)

        x = regex.search(patt, user)
        if x:
            """USER ID IS NUMBER"""
            if '/profile.php' in url2:
                info = user
            else:
                info = url_ps.path[1:]
        else:
            """User id is string"""
            sel = Selector(source)
            pza = sel.xpath("//a[contains(@href,'about')]")
            pzm = sel.xpath("//a[contains(@href,'/more/')]")
            href = pzm.attrib.get('href')

            if href:
                if 'pages' in href:
                    pid = str(href).split('/')
                    # print(pid)
                else:
                    print(href, url)
            else:
                print(f':PAGE_ERROR: {user} {url}')

