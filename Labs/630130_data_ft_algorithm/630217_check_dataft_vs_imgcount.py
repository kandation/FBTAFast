import json
from pprint import pprint
from typing import List, Optional

from parsel import Selector
from pymongo import MongoClient

fb_url_m = 'https://m.facebook.com/'
fb_url_w = 'https://www.facebook.com/'

db_name = 'fbta_20200202_1816'
db_name = 'fbta_20200216_0000'


"""
โค๊ตนี้ทำหน้าที่ พิสูจน์ว่า Data-ft กับ img-count สามารถมีความสัมพันธ์ที่จะช่วยลดรูปใดๆได้บ้าง
แต่ดูเหมือนว่า จะยังอยากอยู่ เช่นถ้าบอกว่า img-attment <= 3 จะไม่มี รูปที่ + เพิ่ม
แต่ความจริงก็ยังมีรูปที่ยาวๆ อีก
"""

if __name__ == '__main__':
    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('05_album_count')
    collection_post = db.get_collection('03_post_page')

    docs_album = collection.find()

    ccc = 0
    collect_list = {str(i):0 for i in range(7)}
    collect_list_gt0 = {str(i):0 for i in range(7)}

    sum_img_count = 0

    for doc in docs_album:
        docs_post = collection_post.find({'_id': doc.get('history')})


        for doc_post in docs_post:
            js = doc_post.get('dataft').get('dataft-raw')
            pp = js.get('photo_attachments_list',[])

            other_local = js.get('story_location')

            sum_img_count += doc.get('img-count')

            if other_local not in [6,9]:
                print(js)

            if doc.get('img-count') > 0:
                collect_list_gt0[str(len(pp))] += 1
                # if len(pp) == 3:
                #     print(js)
            else:
                # if len(pp) == 0:
                #     # เป็นอัลบัมสมัยโบราณในกลุ่มที่ไม่มี +n
                #     print(js)
                collect_list[str(len(pp))] += 1
            if pp:
                ccc += 1

    print(ccc)
    print(collect_list)
    print(collect_list_gt0)
    print(sum_img_count)




        # bs = Selector(doc.get('source', ''))
        # dataft_list: List[Optional[Selector]] = bs.css("div[data-ft]")
        #
        # if len(dataft_list) == 0:
        #     '''อาทิเช่น note'''
        #     pass
        #     #
        #     # # print(dataft_list)
        #     # # print('https://m.facebook.com' + doc['url'])
        #     # if 'story' in doc['url']:
        #     #     # print(doc)
        #     #     # print(doc['source'])
        #
        # else:
        #     dataft = find_max_dataft(dataft_list)
        #     # print(dataft)
        #     dataparse(dataft, doc)

