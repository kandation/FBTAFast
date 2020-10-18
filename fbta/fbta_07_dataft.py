"""
ขั้นตอนนี้ความจริงต้องทำก่อนขั้นที่ 6 แต่ว่ามันเป็นกระบวนการแบบเก่า จะกลับไปแก้ก็เรงว่าจะทำยาก
ทางที่ดีที่สุด ก็ทนๆใช้ไปก่อน จนกว่า จะทำ union ข้อมูลอัลบัมที่ไม่จำเป็นได้
"""

import json
from pprint import pprint
from typing import List, Optional

from parsel import Selector
from pymongo import MongoClient

from fbta.fbta_node_master import FBTANodeMaster


class FBTADataft:
    def __init__(self, node_master: FBTANodeMaster):
        self.fb_url_m = 'https://m.facebook.com/'
        self.fb_url_w = 'https://www.facebook.com/'
        self.__setting = node_master.settings
        self.client = MongoClient()
        self.db = self.client.get_database(self.__setting.db_name)
        self.collection = self.db.get_collection('03_post_page')
        self.parse_data = {}

        self.__doc = None

    def __find_max_dataft(self, dataft_list):
        max_indexx = [len(x.attrib['data-ft']) for x in dataft_list]
        max_index = max_indexx.index(max(max_indexx))
        return dataft_list[max_index].attrib['data-ft']

    def __dataft_reset(self):
        self.parse_data = {
            'dataft-raw': '',
            'dataft-type': '',
            'instruct': []
        }

    def __dataparse(self, ft):
        self.__dataft_reset()

        js = json.loads(ft, encoding='utf8')

        k = js.get('attached_story_attachment_style')
        ppps = ['photo', 'album', 'share', 'video_inline', 'cover_photo', 'animated_image_share', 'profile_media',
                'new_album', 'page_insights', 'animated_image_video', 'video_direct_response', 'commerce_product_item',
                'event', 'video_share_highlighted', 'avatar', 'native_templates', 'note', 'fallback']
        attmaen_othrt = ['unavailable', 'multi_share', 'photo_link_share', 'group_sell_product_item', 'question',
                         'video',
                         'file_upload', 'story_list', 'image_share', 'group']
        if k in ppps and k is not None:
            self.__parse_album_process(js, k)

    def __parse_album_process(self, js, k):
        if k == 'album' or k == 'new_album':
            self.parse_data['dataft-raw'] = js
            self.parse_data['dataft-type'] = k
            self.collection.update_one({'_id': self.__doc.get('_id')}, {'$set': {'dataft': self.parse_data}})

    def main(self):

        # docs = collection.update_many({'dataft-type': 'album'}, {'$unset': {'dataft-raw':None, 'instruct':None,'dataft-type':None}})
        # print(docs)
        docs_post = self.collection.find()

        for doc in docs_post:
            self.__doc = doc
            bs = Selector(self.__doc.get('source', ''))
            dataft_list: List[Optional[Selector]] = bs.css("div[data-ft]")
            if len(dataft_list) == 0:
                '''อาทิเช่น note'''

                # print(dataft_list)
                # print('https://m.facebook.com' + doc['url'])
                if 'story' in self.__doc['url']:
                    '''
                    '''
                    t = 0
                    # print(doc)
                    # print(doc['source'])
                else:
                    pass
                    # print(doc)

            else:
                dataft = self.__find_max_dataft(dataft_list)
                # print(dataft)
                self.__dataparse(dataft)
