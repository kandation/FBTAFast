from parsel import Selector
from pymongo import MongoClient
from urllib.parse import unquote
import fbta.fbta_log as fbta_log
# import bson
import re as regex
from bson import DBRef, ObjectId

fb_url_m = 'https://m.facebook.com/'


def main(db_name):
    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('03_post_page')
    coll_photo = db.get_collection('99_photos_tank')

    key = {'description.story.link-info.type': "photo"}
    docs_post = collection.find(key)

    PHOTO_PATTERN = '\/([0-9]+)\/\?|\?fbid=([0-9]+)|\?story_fbid=([0-9]+)'

    photos_list = {}
    counter = 0

    for doc in docs_post:
        src = DBRef(collection.name, doc.get('_id'), db.name)

        optional = doc['description']['story']['link-info']['optional']
        str_lnk = ''.join(optional)

        fbid_result = regex.findall(PHOTO_PATTERN, str_lnk)

        photo_fbid = ''.join(fbid_result[0])

        if photo_fbid in photos_list:
            photos_list[str(photo_fbid)]['src'].append(src)
        else:
            photos_list[str(photo_fbid)] = {
                'src': [src], 'url': str_lnk
            }
        fbta_log.show_counter(counter, 1000)
        counter += 1

    data_insert = {}

    print('@', counter)
    print(len(photos_list))
    counter = 0

    from bson.objectid import ObjectId

    for photo_key in photos_list:
        data_insert['_id'] = ObjectId()
        data_insert['photo_id'] = photo_key
        data_insert['type'] = 'photo'
        data_insert['url'] = photos_list[photo_key]['url']
        data_insert['ref'] = photos_list[photo_key]['src']

        fbta_log.show_counter(counter, 1000)
        counter += 1

        coll_photo.insert_one(data_insert)


if __name__ == '__main__':
    main('fbta_20200423_0121')