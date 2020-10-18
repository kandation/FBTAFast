from parsel import Selector
from pymongo import MongoClient
from urllib.parse import unquote
import fbta.fbta_log as fbta_log
from bson import DBRef, ObjectId

fb_url_m = 'https://m.facebook.com/'


def main(db_name):
    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('03_post_page')
    coll_album = db.get_collection('98_album_no_duplicate')

    key = {'description.story.link-info.type': "album"}
    docs_post = collection.find(key)

    album_id_set = {}
    counter = 0
    for doc in docs_post:
        src = DBRef(collection.name, doc.get('_id'), db.name)
        album_id = doc['description']['album']['data-album']['album-id']

        album_type = doc['description']['album']['data-album']['album-cluster']['type']

        if album_id in album_id_set:
            album_id_set[str(album_id)]['src'].append(src)
        else:
            album_id_set[str(album_id)] = {
                'src': [src],
                'type': album_type
            }

        fbta_log.show_counter(counter, 1000)
        counter += 1

    print('Fetch Completed Start Insert to DB')

    insert_count = 0
    counter = 0

    for album_set_key in album_id_set:
        insert_data = {'aid': album_set_key, 'ref': album_id_set[album_set_key]['src'],
                       'type': album_id_set[album_set_key]['type']}
        coll_album.insert_one(insert_data)
        insert_count += 1
        fbta_log.show_counter(counter, 1000)
        counter += 1

    print(f'Insert Completed @ {insert_count}')
