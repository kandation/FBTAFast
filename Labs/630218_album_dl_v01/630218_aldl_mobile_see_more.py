from pprint import pprint

from parsel import Selector
from pymongo import MongoClient

from fbta_configs import FBTAConfigs
from fbta_driver import FBTADriver
from fbta_node_master import FBTANodeMaster
from fbta_settings import FBTASettings

db_name = 'fbta_20200216_0000'

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
    #
    # test_url = 'https://m.facebook.com/PixivNiconicoGazou/albums/2152919778138841/'
    # test_url = 'https://m.facebook.com/pandetacademy/albums/3221380814570566'
    # test_url = 'https://m.facebook.com/gianluca.rolli/albums/10218026786918731/'
    # test_url = 'https://m.facebook.com/NonnaNyanNyan/photos/?tab=album&album_id=652802428527639&_rdr'
    # test_url = 'https://m.facebook.com/1175443659329014'

    page_error_topic = ['Content Not Found']

    client = MongoClient()

    db = client.get_database(db_name)
    collection = db.get_collection('05_album_count')
    collection_post = db.get_collection('03_post_page')

    docs_album = collection.find()

    ccc = 0
    collect_list = {str(i): 0 for i in range(7)}
    collect_list_gt0 = {str(i): 0 for i in range(7)}

    for doc in docs_album:
        docs_post = collection_post.find({'_id': doc.get('history')})

        for doc_post in docs_post:
            js = doc_post.get('dataft').get('dataft-raw')
            pp = js.get('tl_objid', [])
            location = js.get('story_location')

            other_local = js.get('story_location')

            if doc.get('img-count') > 0:
                """
                วิธีนี้ยังมีการทำซ้ำอยู่ คือ รู้ว่ารูปภาพคือ pcb หรืออะไรอยู่แล้ว จากครางที่โหลดข้อมูล story มา
                ก็ไปค้นหาในนั้น ไม่ต้องโหลดใหม่
                พอได้ข้อมูลมา จับยัด link เลย
                """
                if location == 9:
                    m_url = f"https://m.facebook.com/{pp}"
                    res = session.get(m_url)
                    sel = Selector(res.text)
                    k = sel.css('#objects_container').css('a > img').xpath('.//..')
                    if session.get_title() not in page_error_topic:
                        try:
                            check_link = k[0].attrib
                        except:
                            print(doc_post)
                            print(session.get_title())
                            exit()


                    """ ถ้าเป็นอับัมรูป มันจะมี role="presentation" นอกนั้นให้เดาเแ็น pcb แต่ถ้าเป็น สนแฟะรนื 6 ก็ oa"""
                    # TODO : ให้กลับไปตรวจสอบข้อมูลในDB ว่าจะเป็นประเภทอะไรกันแน่ จากนั้น ก็ค่อยลงมือทำตัวเก็บภาพแบบทีละ 12
                    """ ซึ่งจากการคำนวนแล้ว มันสามารถแบ่งรูปไปให้แต่ละ cluster ช่วยโหลดได้ ความเร็วก็จะเพิ่มขึ้นมาก
                    แต่ว่าการจะดาวน์โหลดรูปภาพ ควรมีการจัดเก็บด้วยว่า ไม่ใช้อัลบัมที่ซ้ำ จะไได้ไม่ต้องโหลดมาเยอะๆ"""

                    """
                    หารูปภาพได้แล้ว แต่ยังมีปัญหากับ top-level อยู่ เช่นอัลบัมที่ตัวเองแชร์ เจ้า tlstory มันดันเป็นของตัวเอง
                    ไม่ไใช่อัลบัมที่แท้จริง  
                    วิธีแก้ก็ ปรับอัลกอให้เข้า original post ไปเลย
                    ส่วนวิธีการสำรวจ ไม่ควรใช้ตัวนี้สำรวจ แต่ควรจะ filter หาอัลบัมซ้ำตั้งแต่ขั้นตอน 03 load story แล้ว
                    ก็ไปเป็น method  ใหม่ซะนะ
                    """
                    """
                    ปกติแล้วเราจะรู้จำนวนภาพในอัลบัมอยู่แล้ว การทราบ  more_item ก็ไม่จำเป็นเท่าไร
                    อีกทั้งการตรวจประเภทอัลบัม นั้นทำมาตั้งนานแล้ว แทบจะเจอข้อมูลแล้วโดยนให้ find12img ทำงานได้เลย
                    
                    """
                    if '/a.' in check_link.get('href'):
                        url_new = f'https://m.facebook.com/media/set/?set=a.{pp}&type=1'
                        find12img(url_new)
                        # print(check_link)
                    elif 'pcb.' in check_link.get('href'):
                        url_new = f'https://m.facebook.com/media/set/?set=pcb.{pp}&type=1'
                        find12img(url_new)

                    else:

                        print(check_link)



                    #     print(js)
                    # print(k)
                    # exit()
                # print(js)

    # res = session.get(test_url)
    #
    # print(res.text)
    # sel = Selector(res.text)
    # k = sel.css('#m_more_item > a').attrib['href']
    # print(k)
