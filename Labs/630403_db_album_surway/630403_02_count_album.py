from parsel import Selector
from pymongo import MongoClient
from urllib.parse import unquote
# import bson
from bson import DBRef, ObjectId

from fbta_configs import FBTAConfigs
from fbta_driver import FBTADriver
from fbta_node_master import FBTANodeMaster
from fbta_settings import FBTASettings

fb_url_m = 'https://m.facebook.com/'
fb_url_w = 'https://www.facebook.com/'

db_name = 'fbta_20200331_2306'


def find12img(url_new):
    data_ret = {
        'is-more': '',
        'photos': []
    }
    res_new = session.get(url_new)
    sel_new = Selector(res_new.text)
    ks = sel_new.css('#thumbnail_area > a')
    more_items = sel_new.css('#m_more_item > a')

    if more_items:
        more_item_link = more_items[0].attrib.get('href')
        data_ret['is-more'] = more_item_link

    for kps in ks:
        jsp = kps.attrib.get('href')
        data_ret['photos'].append(jsp)

    return data_ret


if __name__ == '__main__':
    images = []

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
    # settings.date_process = [2017, 10, 1]
    settings.dir_path_detail = settings.DIR_DETAIL_NEW_ALL_RUN

    node_master = FBTANodeMaster(settings, configs)
    node_master.start()

    session = FBTADriver(node_master)

    session.add_cookie_from_file()
    session.get('https://m.facebook.com')
    # session.delete_cookie('noscript')
    # session.set_header_chrome()
    session.set_header_firefox()

    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    # }

    page_error_topic = ['Content Not Found']

    client = MongoClient()
    db = client.get_database(db_name)
    # collection = db.get_collection('03_post_page')
    coll_album = db.get_collection('99_album_no_duplicate')

    docs_post = coll_album.find()

    PHOTO_PATTERN = '\/([0-9]+)\/|\?fbid=([0-9]+)'

    url_patt = 'media/set/?set={a_type}.{aid}&type=1'
    allow_type = ['a', 'oa', 'pcb']

    for doc in docs_post:
        a_type = doc.get('type')
        aid = doc.get('aid')

        url = fb_url_m + url_patt.format(a_type=a_type, aid=aid)

        data_insert = {'photo-cluster': [find12img(url)]}

        coll_album.update_one({'_id': doc.get('_id')}, {'$set': data_insert})
