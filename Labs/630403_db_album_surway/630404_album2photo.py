from parsel import Selector
from pymongo import MongoClient
from urllib.parse import unquote
import fbta_log
# import bson
import re as regex
from bson import DBRef
from bson.objectid import ObjectId

fb_url_m = 'https://m.facebook.com/'

db_name = 'fbta_20200404_0410'

if __name__ == '__main__':

    client = MongoClient()
    db = client.get_database(db_name)
    coll_album = db.get_collection('98_album_no_duplicate')
    coll_photo = db.get_collection('99_photos_tank')

    key = {'photo-cluster.0.is-more': ''}
    docs_post = coll_album.find(key)

    PHOTO_PATTERN = '\/([0-9]+)\/\?|\?fbid=([0-9]+)|&id=([0-9]+)&source'

    photos_list = {}
    counter = 0

    for doc in docs_post:
        src = DBRef(coll_album.name, doc.get('_id'), db.name)
        data_insert = {}
        photo_db_list = doc['photo-cluster'][0]['photos']
        for pl in photo_db_list:
            str_lnk = ''.join(pl)
            fbid_result = regex.findall(PHOTO_PATTERN, str_lnk)
            print(fbid_result,pl)
            photo_fbid = ''.join(fbid_result[0])

            data_insert['_id'] = ObjectId()
            data_insert['photo_id'] = photo_fbid
            data_insert['type'] = 'album2photo'
            data_insert['url'] = str_lnk
            data_insert['ref'] = src


            coll_photo.insert_one(data_insert)

        fbta_log.show_counter(counter, 1000)
        counter += 1

    print('@', counter)