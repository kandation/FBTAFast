from parsel import Selector
from pymongo import MongoClient
from urllib.parse import unquote
import fbta_log
# import bson
import re as regex
from bson import DBRef
from bson.objectid import ObjectId

fb_url_m = 'https://m.facebook.com/'


def get_photo_fbid(url):
    PHOTO_PATTERN = '\/([0-9]+)\/\?|\?fbid=([0-9]+)|&id=([0-9]+)&source|\?story_fbid=([0-9]+)'
    fbid_result = regex.findall(PHOTO_PATTERN, url)
    return ''.join(fbid_result[0])


def main(db_name):
    """
    ตัวนี้ยังไม่สมบูรณ์ ถ้ามีกรณีที่ อัลบัมมีวีดีโออยู่ มันก็ไม่รู้นะ มันก็ส่งไปตามปกติ
    :param db_name:
    :return:
    """

    client = MongoClient()
    db = client.get_database(db_name)
    coll_album = db.get_collection('98_album_no_duplicate')
    coll_photo = db.get_collection('99_photos_tank')

    key = {'photo-cluster.0.is-more': ''}
    docs_post = coll_album.find(key)

    photos_list = {}
    counter = 0

    for doc in docs_post:
        src = DBRef(coll_album.name, doc.get('_id'), db.name)
        data_insert = {}
        photo_db_list = doc['photo-cluster'][0]['photos']
        aid = doc['aid']
        for pl in photo_db_list:
            str_lnk = ''.join(pl)
            photo_fbid = get_photo_fbid(str_lnk)
            if 'video' in pl:
                """
                ไม่รู้ใส่มาทำไมแต่อย่าลืมทดสอบหา ลิงก์ที่เป็นวีดีโอด้วย
                แต่ตรวจดูละ ไร้สาระมาก มันไม่มี ถ้าจะมีมันต้องรู้ที่หน้า story แล้ว หรือไม่ก็เข้าไปตรวจตอนโหลดรูป
                """
                pass
            print(photo_fbid, pl)

            # data_insert['_id'] = ObjectId()
            data_insert['photo_id'] = photo_fbid
            data_insert['aid'] = aid
            data_insert['type'] = 'album2photo'
            data_insert['url'] = str_lnk
            data_insert['ref'] = src

            # coll_photo.insert_one(data_insert)

        fbta_log.show_counter(counter, 1000)
        counter += 1

    print('@', counter)


if __name__ == '__main__':
    main('fbta_20200405_0314')
