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
    global icount
    js = json.loads(ft, encoding='utf8')
    k = js.get('attached_story_attachment_style')
    mf_key = js.get('mf_story_key')
    ppps = ['photo', 'album', 'share', 'video_inline', 'cover_photo', 'animated_image_share', 'profile_media',
            'new_album', 'page_insights', 'animated_image_video', 'video_direct_response', 'commerce_product_item',
            'event', 'video_share_highlighted', 'avatar', 'native_templates', 'note','fallback']
    attmaen_othrt = ['unavailable', 'multi_share', 'photo_link_share', 'group_sell_product_item', 'question', 'video',
                     'file_upload', 'story_list', 'image_share', 'group']

    story_att_style_list = ['avatar']
    sas = js.get('story_attachment_style')
    photo_list = js.get('photo_attachments_list')
    page_id = js.get('page_id')
    tn_is_real = js.get('tn')
    # if k in ppps and k is not None:
    #     if k == 'photo':
    #         pass
    #         # print('https://m.facebook.com/'+js['tl_objid'])
    #         # print('https://m.facebook.com/'+js['photo_id'])
    #         # print(js)
    #     if k == 'album':
    #         """
    #         621119
    #         พวก top_level_post ไม่ควรเอามาใช้ เพราะมันจะดึงลำดับถัดไปไม่ใช้ต้นฉบับ ควรมีการหา original_post ด้วย
    #         ส่วนการพิสูจน์ว่าอัลบัมนั้นมีเยอะไหม จะมีการทดสอบ 3 ขั้น (แต่ยังไม่ได้ลองความเร็ว)
    #         ถ้า ความยาวอาเรย์ <= 4 อัลบัมนั้น เอาแทร็กรูปมาได้เลย มีแค่ 4 แน่นอน
    #         ถ้า ความยาว 5 ยังไม่ชัวร์ (แต่สามารถผ่านไปก่อนได้ค่อยไปใช้ คลาสทดสอบทีหลัง)
    #         ----
    #         พอได้ข้อมูลหอมบากหอมคอแล้ว ต้องพิสูจน์ว่ามันเยอะจริงไหม
    #         ความเร็วการโหลดแบบ m เร็วอยู่แล้ว อันไหนเกิน 5 ก็ยิงมา prof เลย
    #         ถ้าเกิดมันเกิน 12 มันจะมี load more ข้างล่าง อาจจะต้อง พิจารณาทางเลือกอื่นๆ
    #         -----
    #         ข้อยากของอันนี้คือ เราไม่มีทางรู้ว่า รูปแบบที่มันมานั้นเป็นอัลบัมแปบบ in post หรือ อัลบัมแยกเลย
    #         ** ปล เนื่องจากเรารู้ว่ามันคืออัลบัมจากตอนเก็บ storyแล้ว ในนั้นจะมีข้อมูลรูปภาพกับลิงค์อยู่ซึ่ง ตัวลิงก์เองจะบอกประภทไว้แล้ว
    #         ให้เราทำการ parse ลิงก์นั้นหาคำ pcb , oa , a  จากนั้นทำการใช้ลิกง์ด้านล่างเพื่ือจัดกลุ่มหาจำนวน
    #
    #         ** แต่มันก็มีข้อสงเกตนิดๆว่า ขั้นตอนรวมกันทั้งหมดอาจจะใช้เวลานาน สุดท้ายแล้ว การเสีย 3 วิจะเป็นทางเลือกที่ดีที่สุดหรือไม่
    #         อาจจะต้องมีการหาจำนวนที่แน่นอน เป็นอัตราส่วน
    #         -----
    #         https://m.facebook.com/media/set/?set=pcb.3058058927751709&type=1
    #         https://m.facebook.com/media/set/?set=a.1869171569782669&type=1
    #         https://m.facebook.com/media/set/?set=oa.2970320783192191
    #         """
    #         pass
    #         try:
    #             if len(js['photo_attachments_list']) <= 4:
    #                 if js['top_level_post_id'] != js['tl_objid']:
    #                     pass
    #                     # print(f"{fb_url_m}{js['tl_objid']} --- {fb_url_w}{doc['url']}")
    #                     # print('https://m.facebook.com/' + js['top_level_post_id'])
    #                     # pprint(js)
    #                     # mf_story_key == top_level_post_id == throwback_story_fbid
    #                     #print('https://m.facebook.com/'+doc['url'],'https://m.facebook.com/' + js['top_level_post_id'],'https://m.facebook.com/' + js['tl_objid'], js)
    #                 else:
    #                     if js.get('page_insights') is None:
    #                         pass
    #                         # ไม่ใช่เพจ ส่วนใหญ่เป็น iamges group
    #                         # เป็นได้ทั้งโพสส่วนตัว และในกลุ่ม มักจะไปโผล่โพสที่มีรายละเอียด
    #                         # print('https://m.facebook.com/' + js['tl_objid'])
    #                         # pprint(js)
    #         except:
    #             pass
    #             # print(doc)
    #
    #
    #     if k == 'cover_photo':
    #         pass
    #         # """สามารถดาวน์โหลดเหมือนูปภาพได้เลย"""
    #         # print(js)
    #         # print(f'{fb_url}{js.get("top_level_post_id")}',ft)
    #
    #     if k == 'new_album':
    #         try:
    #             if len(js['photo_attachments_list']) <= 4:
    #                 if js['top_level_post_id'] != js['tl_objid']:
    #                     pass
    #                     '''จำไม่ได้ว่าวิเคราะห์อะไร'''
    #                     # print('https://m.facebook.com/' + js['tl_objid'], end=' ------ ')
    #                     # print('https://m.facebook.com/' + js['top_level_post_id'])
    #
    #             # """throwback_story_fbid คือ โพสต้นฉบับ // top_level_post_id คือโพสของ Story หรือโพสหลักที่เรา like"""
    #             # """บางที่ประเภท New Album อาจจะหายไป ทำให้เกิดโพสสาบสูญ สามารถตามที่ tag รูป เพื่อพิสูจน์ หรืออาจจะหา story_fbid เพื่อไปอัลบัมต้น"""
    #             # """tl_objid น่าจะไปที่อัลบัมตรงกว่า"""
    #             # """ยังไม่เคยเจอแบบเป็น album ขของ Groups"""
    #             # print(f'{fb_url}{js.get("top_level_post_id")} / {fb_url}{js.get("throwback_story_fbid")}',ft)
    #             # if len(js.get('photo_attachments_list')) <= 4:
    #             #     print(f'{fb_url}{js.get("tl_objid")}' )
    #             # if js.get('top_level_post_id') == '2675550275811457':
    #             #     pass
    #             #     # pprint(js)
    #             #
    #             # if js.get('page_id') is None:
    #             #     """หมายถึง ถ้าอัลบัมนั้น ถูกแชร์โดยผู้ใช้ ไม่ใช้ เพจ"""
    #             #     """tl_objid ไม่ได้หมายความว่าเป็นลิงก์ต้นฉบับ ฉนั้นให้ทำการหา original_content_id"""
    #             #     if js.get('original_content_id') is not None:
    #             #         print(f'{fb_url}{js.get("tl_objid")}', js)
    #         except:
    #             pass
    #             # print(doc)
    #
    #     if k == 'page_insights':
    #         pass
    #         # print(js )
    #
    #     if k == 'avatar':
    #         pass
    #         # print(js)
    # else:
    #     pass
    #     if k is not None:
    #         if k not in attmaen_othrt:
    #             print(js)


    """
    เงื่อนไขต่างๆ
    - sas is None and k is None and page_id is None and og_action_id
    ปกติแล้ว ~(s,k,p ) จะเป็นการบอกว่านั้นเป็นโพสหรือ comment กายๆอยู่แล้ว การมี og_action_id หมายถึงมีการใส่ felling มา
    
    - photo_attachments_list 
    อาจจะหมายถึง โพสที่ถูกแชร์มาจากคนที่โพสในกลุ่ม เป็นภาพหลายๆภาพ 
    
    การระบุด้วย  ~(s,k,p ) อาจจะไม่ใช่คอมเม้นหรือโพสเสมอไปจากกรณี 3060230484050471
    ควรมีการดู simplify กำกับด้วย
    """

    if photo_list:
        """หมายถึงการที่คนในกลุ่ม แชร์โพสที่มีรูปของคนในกลุ่ม"""
        pass

    if mf_key:
        """การไม่มี mf key สนันิฐานว่า อาจจะเป็น note"""
        pass

    if sas is None and k is None and page_id is None:
        print(js)
        icount += 1

    # if k is None:
    #     doc_ref = db.dereference(doc.get('history'))
    #     if doc_ref.get('header').get('simplify') == 'likes':
    #         """
    #         การที่ ไม่มีการระบุไฟล์แนบ และมีการ like อยู่ คือการ like โพส ที่แชร์ โพส ที่มีต้นฉบับมาอีกที
    #         งานนี้ tl_oject ยังอยู่
    #         """
    #         print(fb_url_m+doc.get('url'))
    #         print(js)
    #         print(doc_ref.get('header'))

    # if tn_is_real is None:
    #
    #     """ กรณีที่ js ไม่มี tn (is None) ไม่เคยเจอเลย แสดงว่า tn ปรากฏอยู่ทุกโพส (เพราะจากอัลกลอ) ที่ให้หา data-ft
    #     มันจะเลือกแท๊ก data-ft ที่มากที่สุด ดังนั้นมันจึงไปเอาของใครมาก็ได้ ให้ดูเฉพาะที่  tn == -R พอ
    #     """
    #     print(js)
    #     print(fb_url_m+doc.get('url'))
    #     doc_ref = db.dereference(doc.get('history'))
    #     print(doc_ref.get('header'))


if __name__ == '__main__':
    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('03_post_page')

    docs_post = collection.find()

    icount = 0
    for doc in docs_post:
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
            dataparse(dataft, doc)
    print(icount)

