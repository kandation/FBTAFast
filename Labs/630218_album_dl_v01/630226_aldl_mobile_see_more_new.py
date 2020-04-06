import time
from pprint import pprint

from parsel import Selector
from pymongo import MongoClient

from fbta_configs import FBTAConfigs
from fbta_driver import FBTADriver
from fbta_node_master import FBTANodeMaster
from fbta_settings import FBTASettings

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
    # session.delete_cookie('noscript')
    # session.set_header_chrome()

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }

    page_error_topic = ['Content Not Found']

    client = MongoClient()

    db = client.get_database(db_name)
    collection = db.get_collection('05_album_count')
    collection_post = db.get_collection('03_post_page')

    docs_album = collection.find()

    # db_find_key = {'dataft.dataft-type': {'$exists': True}}
    # docs_post = collection_post.find(db_find_key)

    url_error = []

    ccc = 0
    collect_list = {str(i): 0 for i in range(7)}
    collect_list_gt0 = {str(i): 0 for i in range(7)}

    allow_type = ['a', 'oa', 'pcb']

    start_time = time.time()

    for doc in docs_album:
        docs_post = collection_post.find({'_id': doc.get('history')})

        for doc_post in docs_post:
            js = doc_post.get('dataft').get('dataft-raw')
            pp = js.get('tl_objid')
            if pp is None:
                pass
                """  อนุมานว่าเป็นสิ่งที่ไม่น่าสนใจ (กูแชร์เอง) ลงในกลุ่ม"""
                # print(doc.get('img-count'),f'{fb_url_w}/{js.get("top_level_post_id")}',js)
            else:
                type_of_album = doc_post.get('data-album').get('album-cluster').get('type')
                if type_of_album in allow_type:
                    """ พวกที่เป็นอัลบัม URL อาจจะใช้ tlstory ไปเลย เพราะ pcb ไม่มีหน้าที่ต่อเนื่อง
                    https://m.facebook.com/media/set/?set=pcb.2496478230385330&type=1  
                    เป็น pcb +9 แต่ดันไม่มีข้อมูลอีก --- สรุปมันเป็นรูปที่ผมแชร์ ฉะนั้น  tlobject จึงเป็นของโพสที่ผมแชร์
                    https://m.facebook.com/story.php?story_fbid=2495165603849926&id=100000695314425&_rdr
                    เป็นแชร์ก็จริง แต่เพจนี้ส่วนใหญ่จะเป็น added album ลองไปดูใน dataft เพื่อพิจารณษดู
                    """
                    url_new = f'https://m.facebook.com/media/set/?set={type_of_album}.{pp}&type=1'
                    try:
                        find12img(url_new)
                    except:
                        url_error.append(url_new)
    print(url_error)
    print(len(url_error))
    print('FInish', time.time() - start_time)

    # TODO: 630226 ว่างๆ ก็กลับไป migrate DB ด้วย ให้มันรู้หน่อยว่ามันคือ Comment / Like แล้วใน 1 โพส ก็ไม่ต้องหาซ้ำหรอก
    """
    บางครั้งอัลบัมก็มาจากบุคคล ควรมีเท๊กเอาไว้ก็ดี ie https://m.facebook.com/torasanthai/albums/1879495098803753/?refid=52&__tn__=CH-R
    https://m.facebook.com/media/set/?set=a.2013851491981342&type=1 
    """

    # res = session.get(test_url)
    #
    # print(res.text)
    # sel = Selector(res.text)
    # k = sel.css('#m_more_item > a').attrib['href']
    # print(k)
