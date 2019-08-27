import json
from typing import List, Optional

from parsel import Selector
from pymongo import MongoClient


def dataparse(ft):
    js = json.loads(ft, encoding='utf8')
    k = js.get('attached_story_attachment_style')
    ppps = ['photo', 'album', 'share', 'video_inline', 'cover_photo', 'animated_image_share', 'profile_media',
            'new_album', 'page_insights', 'animated_image_video', 'video_direct_response', 'commerce_product_item',
            'event', 'video_share_highlighted','avatar','native_templates','note']
    if k in ppps and k is not None:
        if k == 'photo':
            # print('https://m.facebook.com/'+js['tl_objid'])
            print('https://m.facebook.com/'+js['photo_id'])
            # print(js)


if __name__ == '__main__':
    client = MongoClient()
    db = client.get_database('fbta_20190825_1941')
    collection = db.get_collection('03_post_page')

    pppppp = collection.find({})
    for doc in pppppp:
        bs = Selector(doc.get('source',''))
        dataft_list: List[Optional[Selector]] = bs.css("div[data-ft]")
        if len(dataft_list) == 0:
            print('https://m.facebook.com' + doc['url'])
            if 'story' in doc['url']:
                print(doc['source'])
        else:
            max_indexx = [len(x.attrib['data-ft']) for x in dataft_list]
            max_index = max_indexx.index(max(max_indexx))
            dataparse(dataft_list[max_index].attrib['data-ft'])
