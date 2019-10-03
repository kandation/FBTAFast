import json
from pprint import pprint
from typing import List, Optional

from parsel import Selector
from pymongo import MongoClient


def dataparse(ft, doc):
    js = json.loads(ft, encoding='utf8')
    k = js.get('attached_story_attachment_style')
    ppps = ['photo', 'album', 'share', 'video_inline', 'cover_photo', 'animated_image_share', 'profile_media',
            'new_album', 'page_insights', 'animated_image_video', 'video_direct_response', 'commerce_product_item',
            'event', 'video_share_highlighted', 'avatar', 'native_templates', 'note']
    if k in ppps and k is not None:
        if k == 'photo':
            pass
            # print('https://m.facebook.com/'+js['tl_objid'])
            # print('https://m.facebook.com/'+js['photo_id'])
            # print(js)
        if k == 'album':
            if len(js['photo_attachments_list']) >= 4:
                if js['top_level_post_id'] != js['tl_objid']:
                    pass
                    # mf_story_key == top_level_post_id == throwback_story_fbid
                    #print('https://m.facebook.com/'+doc['url'],'https://m.facebook.com/' + js['top_level_post_id'],'https://m.facebook.com/' + js['tl_objid'], js)
                else:
                    if js.get('page_insights') is None:
                        # ไม่ใช่เพจ ส่วนใหญ่เป็น iamges group
                        # เป็นได้ทั้งโพสส่วนตัว และในกลุ่ม มักจะไปโผล่โพสที่มีรายละเอียด
                        print('https://facebook.com/' + js['tl_objid'])
                        pprint(js)


if __name__ == '__main__':
    client = MongoClient()
    db = client.get_database('fbta_20190825_1941')
    collection = db.get_collection('03_post_page')

    pppppp = collection.find({})
    for doc in pppppp:
        bs = Selector(doc.get('source', ''))
        dataft_list: List[Optional[Selector]] = bs.css("div[data-ft]")
        if len(dataft_list) == 0:
            # print(dataft_list)
            print('https://m.facebook.com' + doc['url'])
            if 'story' in doc['url']:
                print(doc['source'])
        else:
            max_indexx = [len(x.attrib['data-ft']) for x in dataft_list]
            max_index = max_indexx.index(max(max_indexx))
            dataparse(dataft_list[max_index].attrib['data-ft'], doc)
