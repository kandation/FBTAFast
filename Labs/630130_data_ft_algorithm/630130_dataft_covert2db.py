import json
from pprint import pprint
from typing import List, Optional

from parsel import Selector
from pymongo import MongoClient

fb_url_m = 'https://m.facebook.com/'
fb_url_w = 'https://www.facebook.com/'

db_name = 'fbta_20200202_1816'


def find_max_dataft(dataft_list):
    max_indexx = [len(x.attrib['data-ft']) for x in dataft_list]
    max_index = max_indexx.index(max(max_indexx))
    return dataft_list[max_index].attrib['data-ft']


def dataparse(ft, doc):
    parse_data = {
        'dataft-raw': '',
        'dataft-type': '',
        'instruct': []
    }
    js = json.loads(ft, encoding='utf8')
    k = js.get('attached_story_attachment_style')
    ppps = ['photo', 'album', 'share', 'video_inline', 'cover_photo', 'animated_image_share', 'profile_media',
            'new_album', 'page_insights', 'animated_image_video', 'video_direct_response', 'commerce_product_item',
            'event', 'video_share_highlighted', 'avatar', 'native_templates', 'note', 'fallback']
    attmaen_othrt = ['unavailable', 'multi_share', 'photo_link_share', 'group_sell_product_item', 'question', 'video',
                     'file_upload', 'story_list', 'image_share', 'group','stream_publish']
    if k in ppps and k is not None:
        if k == 'album' or k=='new_album' :
            parse_data['dataft-raw'] = js
            parse_data['dataft-type'] = k
            # collection.update_one({'_id': doc.get('_id')}, {'$set': {'dataft': parse_data}})

    if k in attmaen_othrt and k is not None:
        if k == 'image_share':
            print(js)
    # if k not in ppps+attmaen_othrt and k is not None:
    #     print(js)

if __name__ == '__main__':
    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('03_post_page')
    # docs = collection.update_many({'dataft-type': 'album'}, {'$unset': {'dataft-raw':None, 'instruct':None,'dataft-type':None}})
    # print(docs)
    docs_post = collection.find()

    for doc in docs_post:
        bs = Selector(doc.get('source', ''))
        dataft_list: List[Optional[Selector]] = bs.css("div[data-ft]")
        if len(dataft_list) == 0:
            '''อาทิเช่น note'''

            # print(dataft_list)
            # print('https://m.facebook.com' + doc['url'])
            if 'story' in doc['url']:
                '''
                '''
                t = 0
                # print(doc)
                # print(doc['source'])
            else:
                pass
                # print(doc)

        else:
            dataft = find_max_dataft(dataft_list)
            # print(dataft)
            dataparse(dataft, doc)
