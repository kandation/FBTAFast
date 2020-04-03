import m_630403_album_vote as vote
import m_630403_data_scan as scan
import m_630403_dataft as dataft
from parsel import Selector
from pymongo import MongoClient
from urllib.parse import unquote
import bson

"""
โปรแกรมคำนวนว่าหน้า story บอกว่าเป็นภาพ หรืออะไร (    สมบูรณ์)
แต่ว่าเพื่อความชัวร์ ใช้ data-ft  มาช่วยด้วยก็ดี เผื่อบางที่ไม่มีภาพแสดงตัวอย่าง
@return data_pp
"""

fb_url_m = 'https://m.facebook.com/'
fb_url_w = 'https://www.facebook.com/'

db_name = 'fbta_20200331_2306'

if __name__ == '__main__':
    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('03_post_page')

    docs_post = collection.find()

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
