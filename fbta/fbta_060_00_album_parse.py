import fbta.fbta_060_01_album_vote as vote
import fbta.fbta_060_02_album_scan as scan
import fbta.fbta_060_03_dataft as dataft
import fbta.fbta_log as fbta_log
from parsel import Selector
from pymongo import MongoClient
from urllib.parse import unquote
import bson

fb_url_m = 'https://m.facebook.com/'


def main(db_name):
    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('03_post_page')

    docs_post = collection.find()

    counter = 0
    for doc in docs_post:
        m_source = doc.get('source', '')
        data_pp = scan.data_classify(m_source)
        data_ft_raw = dataft.find_dataft(m_source)

        album_data_vote = {}
        if data_pp['link-info']['type'] == 'album':
            ft_raw = data_ft_raw.get('dataft-type')
            album_data_vote = vote.find_album_id(data_pp['link-info']['optional'], ft_raw)

        data_insert = {
            'description': {
                'story': data_pp,
                'album': album_data_vote,
                'ft': data_ft_raw,
            }
        }

        collection.update_one({'_id': doc.get('_id')}, {'$set': data_insert})
        fbta_log.show_counter(counter, 1000)
        counter += 1
