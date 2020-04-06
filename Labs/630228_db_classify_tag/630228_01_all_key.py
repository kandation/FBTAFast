import json
from pprint import pprint
from typing import List, Optional

from parsel import Selector
from pymongo import MongoClient

fb_url_m = 'https://m.facebook.com/'
fb_url_w = 'https://www.facebook.com/'

db_name = 'fbta_20200202_1816'


# db_name = 'fbta_20200226_1437'

def find_by_key(data, target):
    for key, value in data.items():
        if isinstance(value, dict):
            yield from find_by_key(value, target)
        elif key == target:
            yield value


def find_max_dataft(dataft_list):
    max_indexx = [len(x.attrib['data-ft']) for x in dataft_list]
    max_index = max_indexx.index(max(max_indexx))
    return dataft_list[max_index].attrib['data-ft']


def binaryToDecimal(binary):
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while (binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    print(decimal)


# def classify_scluter():
#     type_arg = ''.join(datft_argument)
#
#     if type_arg not in type_of_argument:
#         type_of_argument[type_arg] = 1
#     else:
#         type_of_argument[type_arg] += 1

#
# def classify_type_couting():
#     for key in js:
#         # if key not in dataft_tag_all:
#         #     print(f'InsertKey= {key}')
#         #     dataft_tag_all.append(key)
#
#         datft_argument[dataft_tag_all.index(key)] = '1'

if __name__ == '__main__':
    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('03_post_page')

    docs_post = collection.find()

    dataft_tag_all = ['mf_story_key', 'top_level_post_id', 'tl_objid', 'throwback_story_fbid', 'story_location',
                      'story_attachment_style', 'tn', 'content_owner_id_new', 'page_id', 'page_insights', 'photo_id',
                      'tagged_locations', 'attached_story_attachment_style', 'photo_attachments_list',
                      'original_content_id', 'original_content_owner_id', 'call_to_action_type', 'ref', 'qid', 'src',
                      'view_time', 'filter', 'og_action_id', 'group_id', 'text_formatting', 'media_with_effects_id',
                      'profile_picture_overlay_owner', 'profile_picture_overlay_id']

    print(len(dataft_tag_all))

    type_of_argument = {
        '1111111000000000000000000000': 645,  # Add friend , follow Person, join group
        '1111101100000000000000000000': 2217,  # ข้อความบน timeline
        '1111111011000000000000000000': 1076,  # Like page story_attachment_style': 'avatar'
        '1111111100100000000000000000': 6759,  # เราที่โพสรูปบน timeline ตัวเอง 1 รูป
        '1111101000000000000000000000': 4567,
        # ไป coment/like ที่โพสชาวบ้าน ที่ไม่ใช่โพสที่มีรูปโดยตรง สามารถสำรวจได้ทาง tl object เพื่อเข้าหาต้นฉบับ จะมาในรูปแบบคนที่โพสในกลุ่ม
        '1111111100000000000000000000': 998,  # แชร์ลิงก์ภายนอก หรือ แชร์อะไรก็ได้ ที่โดนแบนไปแล้ว
        '1111111011010000000000000000': 2,  # life event
        '1111101000101000000000000000': 18424,
        # เราโพสรูปใดๆ 1 รูป หรือ ไลค์รูปใดๆ 1 รูป เท๊คหลัก photo_id, attached_story_attachment_style
        '1111111111110000000000000000': 7203,
        # เราเพิ่มรูปภาพลงอัลบัม ทีละ 1 ภาพ หรืออับโหลดภาพ พร้อมมีการติดแท๊ก สถานที่ และมันจะลงไปอยู่ใน page_id เอาจริงๆนะ ไม่ต้องโหลดก็ได้
        '1111101011101000000000000000': 27847,
        # page_id ที่มี 1รูป และ มีแท๊กสำคัญอย่าง photo_id, attached_story_attachment_style
        '0100101100000000000000000000': 261,  # โพส หรือตอบกลับในกลุ่ม ซึ่งไม่มี tlobject และ story_location=6
        '0000001000000000000000000000': 444,
        # Lagency รูปภาพที่ไปโพสลงบนวอล์คนอื่น และรูปที่อัพเพิ่มเข้าไปในอัลบัม (ไม่มีแท๊กเลย)
        '1111101000001000000000000000': 2120,
        # ส่วนใหญ่จะเป็นการไปกระทำกับ ลิงก์ที่คนอื่นแชร์ แต่ก็มีส่วนน่าสนใจคือ attached_story_attachment_style=animated_image_share
        '0100111100000000000000000000': 145,
        # ส่วนใหญ่เป็นเหตการณ์ที่เกิดขึ้นในกลุ่ม มี story_attachment_style หลายแบบ และรวมถึงอัลบัมที่โบราณมากๆ สำคัญสุดน่าจะเป็นการบอกว่าเป็น note เสียมากกว่า
        '0100111100100000000000000000': 174,
        # เป็นภาพที่โพสเองในกลุ่ม มี 'photo_id': '558936454139527' เป็นสำคัญ และ 'story_attachment_style': 'photo' ไม่ต้องโหลดก็ได้
        '1111101011111100000000000000': 47,
        # 'photo_attachments_list':, 'attached_story_attachment_style': 'new_album' ที่มี tagged_locations ใช้วิธีปกติเลย
        '1111101011111000000000000000': 286,
        # รูปภาพใดๆที่มีแท๊กสถานที่  'tagged_locations': 'attached_story_attachment_style': 'photo'
        '1111101100101100000000000000': 4,
        '1111101011001000000000000000': 880, # การ like หรือ กระทำใดๆ บนเพจ ที่มีการแชร์ลิงก์ หาได้จาก 'page_insights':
        '0100101100101100000000000000': 5,
        '0000111100000000000000000000': 1,
        '1111101111111100000000000000': 3,
        '1111101111101000000000000000': 30,
        '1111101100101000000000000000': 14,
        '1111101000101100000000000000': 138,
        '0100101100101000000000000000': 9,
        '1111101011101100000000000000': 649, #
        # New_album และมีแท็ก 'photo_attachments_list': ใช้การดาวน์โหลดปกติได้เลย
        '1111101111111000000000000000': 2, # รูปภาพจากการแชร์  ของที่ตัวเองไปโพสบน วอร์ คนอื่น แต่อย่าไปสนใจ
        '1111101011000000000000000000': 5062,
        # ***สำคัญ*** เป็นโพสที่คนแชร์ เพจที่มีรูปลงในกลุ่ม/ในเพจ แต่ ดันไม่มีแท๊กหารูป และใช้ tl_object ไม่ได้ ***
        # ให้หาแท็ก a > img เพื่อเข้าไปยังหน้าหลักของมัน แต่ก็ต้องตรวจสอบด้วยว่ามันเป็นภาพ หรือวีดีโอ ,
        # หรือ ถ้าต้องการใช้เวลามากขึ้น เพื่อเก็บ dataft จำเป็นต้องเข้าไปยัง top_level_post_id เพื่อรวบรวม (
        # และไม่น่าจะมี nest ที่ลึกกว่านี้แล้ว)
        '0100101111111000000000000000': 1,
        '1111111100110000000000000000': 399,
        '1111101111101011000000000000': 1179,
        # เป็นการแชรโพส มี 'photo_id': ใช้ได้เลย , แต่ 'attached_story_attachment_style': อาจจะไม่ใช่ Photo เสมอไป
        '1111101100101011000000000000': 154,
        # ลแชร์ลิงก์หรือวดีโอบนวอลตัวเอง มีแท๊ก  'original_content_id':  เพื่อเข้าถึงลิงก์หลักได้เลย ส่วนใหญ่จะเป็นลิงก์เดียว
        # แยกแยะด้วย 'attached_story_attachment_style': 'video_inline' ก็ได้
        '0100101100101011000000000000': 14,
        '1111101111101010000000000000': 71,
        # การแชร์พร้อมคอมเม้นผมเอง 'photo_id': '529018587304330', ==  'original_content_id':  gเข้าลิงก์หลักแล้วโหลดได้เลย
        '1111101000000100000000000000': 283,
        # การที่เรากด like รูปที่คนอื่นแชร์ มี photo_attachments_list ให้ตรวจสอบว่าเป็นอัลบัม
        # ให้เข้าไปยัง tl_object แล้ว renew Tag ใหม่
        '1111111100000011000000000000': 73,
        '0100111100000000100000000000': 16,
        '1111101111111010000000000000': 3,
        '1111111111010000000000000000': 14,
        '0000111000100000000000000000': 1,
        '1111111100100000010000000000': 2,
        '0100101111111110000000000000': 1,
        '1111101111000000000000000000': 7,
        '0100111100000011000000000000': 4,
        '1111111000000000010000000000': 164,
        # อย่าไปสนใจ แค่พวก 'story_attachment_style': 'fallback',
        '0100111100100100000000000000': 13,
        '1100111111000100001111000000': 1,
        '1111101111111011000000000000': 14,
        '1111101111000011000000000000': 9,
        '1111101000001100000000000000': 3078,  # Album รูปธรรมดา ส่วนใหญ่เป็นแบบ cluster album เข้าถึงโดดยตรงเลย
        '0100101111101011000000000000': 5,
        '1111101111101110000000000000': 156,
        '0100101111111010000000000000': 1,
        '1111101100000011000000000000': 7,
        '1111101100101010000000000000': 21,
        '1111101011011100000000000000': 56,
        '1111101011011000000000000000': 41,
        '1111101100101110000000000000': 22,
        '0100101111101010000000000000': 1,
        '1111111111000000000000000000': 1,
        '1111111100000100000000000000': 30,
        '1111111111100000000000000000': 3,
        '1111101000111000000000000000': 3,
        '0100111100000100000000000000': 8,
        '0100101100001100000000000000': 1,
        '1111111000100000010000000000': 3,
        '1111101100000000000000100000': 18,
        '1111111000010000000000000000': 3,
        '1111111100010000000000000000': 1,
        '1111101111001111000000000000': 148,
        '1111101111101100000000000000': 1,
        '0100101100001000000000000000': 1,
        '1111101011000100000000000000': 2031,
        # การกดไลค์ โพส ที่เป็นอัลบัมท ี่คนอื่น/เพจ แชร์ บางที่โพสที่คนอื่นแชร์ก็หาย ทำให้ไม่สามารถติดตามผผ่านกากดลิงก์ได้
        # ให้ลองมองหาแท๊ก 'originalPostOwnerID': '1944268745788721'
        # ตัวนี้จะแตกต่างกับอีกตัวคือเป็นโพสสมัยใหม่ ที่มี  'photo_attachments_list' บอกว่าเป็นอัลบัมรูปเลย ไม่ต้องเดา
        '0100101111101100000000000000': 1,
        '1111101011001100000000000000': 5570,  # album ธรรมดาเลย ใช้ตัวที่มีอยู่แล้วได้เลย
        '0100101111001111000000000000': 1,
        '0100101111101000000000000000': 2,
        '0100101111001100000000000000': 1,
        '1111101100001100000000000000': 1,
        '1111111000100000000000000000': 1962,  # watched a video 'story_attachment_style': 'video_inline'
        '1111111000100000100000000000': 263,
        # watched a video 'story_attachment_style': 'video_inline' +'call_to_action_type': 'WATCH_MORE'
        '1111101111001100000000000000': 2,
        '1111101111001011000000000000': 26,
        '1111101100001011000000000000': 8,
        '1111111111010000000000100000': 3,
        '1110101100000000001101010000': 1, # Events
        '1111111100000000000000100000': 3,
        '0100101111101110000000000000': 1,
        '1111111100100000000000100000': 5,
        '0100101100000000000000100000': 1,
        '0100101100101110000000000000': 1,
        '1111101100000000000000001000': 190,
        # การโพสหน้าวอลตัวเองโดยใช้พื้นหลัง 'text_formatting':
        '1111101100001111000000000000': 37,
        # การแชร์อัลบัมบนหน้าวอลตัวเอง 'attached_story_attachment_style': 'album' สามารถใช้อันเดิม หรือ
        # 'original_content_id': '10156614964180766'
        '1111111100100000000000000100': 2,
        '1111101111001110000000000000': 1,
        '1111101100000000000000101000': 24, # โพสตัวเอง 'text_formatting':
        '1111101111101011000000100000': 1,
        '0100101100000000000000001000': 6,
        '0000111000000000000000000000': 8,
        '1111101011010000000000000000': 1,
        '1111101111000111000000000000': 1,
        '1111101111111011000000100000': 1,
        '1111111100100000000000000111': 2,
        '0100101100001111000000000000': 2}

    # analys_data = {
    #     'person':
    # }

    # """ Excel analysis """
    # print('_', end='\t')
    # for _label in dataft_tag_all:
    #     print(_label,end='\t')
    # print()
    # for _key in type_of_argument:
    #     print(type_of_argument[_key], end='\t')
    #     for _key_each in _key:
    #         print(_key_each, end='\t')
    #     print()
    #
    # exit()

    is5000 = False
    is2000 = False

    icount = 0
    for doc in docs_post:
        datft_argument = ['0' for _ in range(len(dataft_tag_all))]
        bs = Selector(doc.get('source', ''))
        dataft_list: List[Optional[Selector]] = bs.css("div[data-ft]")

        if len(dataft_list) == 0:
            '''อาทิเช่น note'''
            pass
            #
            # # print(dataft_list)
            # # print('https://m.facebook.com' + doc['url'])
            # if 'story' in doc['url']:
            #     # print(doc)
            #     # print(doc['source'])

        else:
            dataft = find_max_dataft(dataft_list)
            # print(dataft)
            js = json.loads(dataft, encoding='utf8')

            for key in js:
                if key in dataft_tag_all:
                    datft_argument[dataft_tag_all.index(key)] = '1'

            type_arg = ''.join(datft_argument)

            # if type_arg == '1111101011000000000000000000':
            #     print(js)
            #
            #     px = [x for x in find_by_key(js, "originalPostOwnerID")]
            #     py= [x for x in find_by_key(js, "story_fbid")]
            #     pz= [x for x in find_by_key(js, "dm")]
            #     print(px,py,pz)
            #     print(fb_url_w+doc.get('url'))
            #     print('-'*50)

            # if type_arg == '1111101011000000000000000000':
            #     print(js)
            #
            #     px = [x for x in find_by_key(js, "originalPostOwnerID")]
            #     py= [x for x in find_by_key(js, "story_fbid")]
            #     pz= [x for x in find_by_key(js, "dm")]
            #     print(px,py,pz)
            #     print(fb_url_w+doc.get('url'))
            #     print('-'*50)

            # """ Comparep betewwen 2 tag album share  by other"""
            # if type_arg == '1111101011000100000000000000' and not is2000:
            #     is2000 = True
            #     print(2000, js)
            #
            #     # px = [x for x in find_by_key(js, "originalPostOwnerID")]
            #     # py= [x for x in find_by_key(js, "story_fbid")]
            #     # pz= [x for x in find_by_key(js, "dm")]
            #     # print(px,py,pz)
            #     print(fb_url_w + doc.get('url'))
            #     print('-' * 50)
            # if type_arg == '1111101011000000000000000000' and not  is5000:
            #     is5000 = True
            #     print(5000, js)
            #
            #     # px = [x for x in find_by_key(js, "originalPostOwnerID")]
            #     # py= [x for x in find_by_key(js, "story_fbid")]
            #     # pz= [x for x in find_by_key(js, "dm")]
            #     # print(px,py,pz)
            #     print(fb_url_w + doc.get('url'))
            #     print('-' * 50)

            """ Normal Test"""

            if type_arg == '1110101100000000001101010000':
                print(js)

                # px = [x for x in find_by_key(js, "originalPostOwnerID")]
                # py= [x for x in find_by_key(js, "story_fbid")]
                # pz= [x for x in find_by_key(js, "dm")]
                # print(px,py,pz)
                print(fb_url_w + doc.get('url'))
                print('-' * 50)

    print(type_of_argument)
