import json
from pprint import pprint
from typing import List, Optional

from parsel import Selector
from pymongo import MongoClient

fb_url_m = 'https://m.facebook.com/'
fb_url_w = 'https://www.facebook.com/'


def dataparse(ft, doc):
    js = json.loads(ft, encoding='utf8')
    k = js.get('attached_story_attachment_style')
    ppps = ['photo', 'album', 'share', 'video_inline', 'cover_photo', 'animated_image_share', 'profile_media',
            'new_album', 'page_insights', 'animated_image_video', 'video_direct_response', 'commerce_product_item',
            'event', 'video_share_highlighted', 'avatar', 'native_templates', 'note']
    attmaen_othrt = ['unavailable', 'multi_share', 'photo_link_share', 'group_sell_product_item', 'question', 'video',
                     'file_upload', 'story_list','image_share','group']
    if k in ppps and k is not None:
        if k=='profile_media':
            """โหลดแบบ Photo/ cover ได้เลย"""
            if js.get('tl_objid') is None:
                print(js)
            else:
                print('https://m.facebook.com/' + js['tl_objid'])
        if k == 'photo':
            pass
            # print('https://m.facebook.com/'+js['tl_objid'])
            # print('https://m.facebook.com/'+js['photo_id'])
            # print(js)
        if k == 'album':
            """
            621119
            พวก top_level_post ไม่ควรเอามาใช้ เพราะมันจะดึงลำดับถัดไปไม่ใช้ต้นฉบับ ควรมีการหา original_post ด้วย
            ส่วนการพิสูจน์ว่าอัลบัมนั้นมีเยอะไหม จะมีการทดสอบ 3 ขั้น (แต่ยังไม่ได้ลองความเร็ว)
            ถ้า ความยาวอาเรย์ <= 4 อัลบัมนั้น เอาแทร็กรูปมาได้เลย มีแค่ 4 แน่นอน
            ถ้า ความยาว 5 ยังไม่ชัวร์ (แต่สามารถผ่านไปก่อนได้ค่อยไปใช้ คลาสทดสอบทีหลัง)
            ----
            พอได้ข้อมูลหอมบากหอมคอแล้ว ต้องพิสูจน์ว่ามันเยอะจริงไหม
            ความเร็วการโหลดแบบ m เร็วอยู่แล้ว อันไหนเกิน 5 ก็ยิงมา prof เลย
            ถ้าเกิดมันเกิน 12 มันจะมี load more ข้างล่าง อาจจะต้อง พิจารณาทางเลือกอื่นๆ
            -----
            ข้อยากของอันนี้คือ เราไม่มีทางรู้ว่า รูปแบบที่มันมานั้นเป็นอัลบัมแปบบ in post หรือ อัลบัมแยกเลย
            ** ปล เนื่องจากเรารู้ว่ามันคืออัลบัมจากตอนเก็บ storyแล้ว ในนั้นจะมีข้อมูลรูปภาพกับลิงค์อยู่ซึ่ง ตัวลิงก์เองจะบอกประภทไว้แล้ว
            ให้เราทำการ parse ลิงก์นั้นหาคำ pcb , oa , a  จากนั้นทำการใช้ลิกง์ด้านล่างเพื่ือจัดกลุ่มหาจำนวน
            
            ** แต่มันก็มีข้อสงเกตนิดๆว่า ขั้นตอนรวมกันทั้งหมดอาจจะใช้เวลานาน สุดท้ายแล้ว การเสีย 3 วิจะเป็นทางเลือกที่ดีที่สุดหรือไม่
            อาจจะต้องมีการหาจำนวนที่แน่นอน เป็นอัตราส่วน
            -----
            https://m.facebook.com/media/set/?set=pcb.3058058927751709&type=1
            https://m.facebook.com/media/set/?set=a.1869171569782669&type=1
            https://m.facebook.com/media/set/?set=oa.2970320783192191
            
            รูปจาก comment 
            https://www.facebook.com/photo.php?fbid=804049202972437&set=p.804049202972437&type=3&theater
            """
            pass
            # if js.get('photo_attachments_list') is None:
            #     """
            #     เป็นอัลบัมสมัยโบราณที่ไม่มีการระบุรูปย่อในนั้น 674525849240134 พบในกลุ่มเก่าๆ
            #     คือมันเป็นประเภท ms.c.e คือมันเป็นรูปภาพเก่า ที่เลื่อนไม่ได้ในเฟส ไม่ต้องสนใจก็ได้
            #     """
            #     print(js)
            if len(js.get('photo_attachments_list',[])) <= 4:

                if js.get('tl_objid') is None:
                    """
                    มีกรณีที่ไม่มี tl_object ด้วย น่าแปลก
                    3026456444050143 :: คือไม่มี tl เพราะ  เราแชร์เข้ากลุ่มลับตัวเอง โดยแชร์มาจากเจ้าของคนอื่นอีกที
                    ดังนั้นมันจึงไม่เกิดขึ้นที่ timeline จึงไม่มี tl_object ไงละ 
                    สรุป แชร์รูปภาพจากอะไรก็ได้ ลงกลุ่ม ด้วยตัวเอง 
                    ถ้าอยากดูโพสตัวเองก็ top_level_post_id ดูโพสต้นทาง original_content_id
                    """
                    pass
                    # print(js)
                # if js['top_level_post_id'] != js['tl_objid']:
                #     """
                #     Page album ธรรมดา แต่ไม่ธรรมาด คือ ต้นทางของ timeline อาจจะมาจาก .... รอว่าง
                #     แต่อาจจะใช้การพิสูจน์ด้วย story_location
                #     """
                #     pass
                #     # print('https://m.facebook.com/' + js['tl_objid'], end =' ----- ')
                #     # # print('https://m.facebook.com/' + js['top_level_post_id'])
                #     # pprint(js)
                #     # mf_story_key == top_level_post_id == throwback_story_fbid
                #     #print('https://m.facebook.com/'+doc['url'],'https://m.facebook.com/' + js['top_level_post_id'],'https://m.facebook.com/' + js['tl_objid'], js)
                # else:
                #     if js.get('page_insights') is None:
                #         pass
                #         # ไม่ใช่เพจ ส่วนใหญ่เป็น iamges group
                #         # เป็นได้ทั้งโพสส่วนตัว และในกลุ่ม มักจะไปโผล่โพสที่มีรายละเอียด
                #         # print('https://m.facebook.com/' + js['tl_objid'])
                #         # pprint(js)

        if k == 'cover_photo':
            pass
            # """สามารถดาวน์โหลดเหมือนูปภาพได้เลย"""
            # print(js)
            # print(f'{fb_url}{js.get("top_level_post_id")}',ft)

        # if k == 'new_album':
        #     pass
        #     if len(js['photo_attachments_list']) <= 4:
        #         if js['top_level_post_id'] != js['tl_objid']:
        #             pass
        #             print('https://m.facebook.com/' + js['tl_objid'], end=' ------ ')
        #             print('https://m.facebook.com/' + js['top_level_post_id'])

            # """throwback_story_fbid คือ โพสต้นฉบับ // top_level_post_id คือโพสของ Story หรือโพสหลักที่เรา like"""
            # """บางที่ประเภท New Album อาจจะหายไป ทำให้เกิดโพสสาบสูญ สามารถตามที่ tag รูป เพื่อพิสูจน์ หรืออาจจะหา story_fbid เพื่อไปอัลบัมต้น"""
            # """tl_objid น่าจะไปที่อัลบัมตรงกว่า"""
            # """ยังไม่เคยเจอแบบเป็น album ขของ Groups"""
            # print(f'{fb_url}{js.get("top_level_post_id")} / {fb_url}{js.get("throwback_story_fbid")}',ft)
            # if len(js.get('photo_attachments_list')) <= 4:
            #     print(f'{fb_url}{js.get("tl_objid")}' )
            # if js.get('top_level_post_id') == '2675550275811457':
            #     pass
            #     # pprint(js)
            #
            # if js.get('page_id') is None:
            #     """หมายถึง ถ้าอัลบัมนั้น ถูกแชร์โดยผู้ใช้ ไม่ใช้ เพจ"""
            #     """tl_objid ไม่ได้หมายความว่าเป็นลิงก์ต้นฉบับ ฉนั้นให้ทำการหา original_content_id"""
            #     if js.get('original_content_id') is not None:
            #         print(f'{fb_url}{js.get("tl_objid")}', js)

        if k == 'page_insights':
            pass
            # print(js )

        if k =='avatar':
            pass
            # print(js)
    else:
        pass
        # if k is not None:
        #     if k not in attmaen_othrt:
        #         print(js)


if __name__ == '__main__':
    client = MongoClient()
    # db = client.get_database('fbta_20191111_1236')
    # db = client.get_database('fbta_20191114_1901_full')
    # db = client.get_database('fbta_20191029_0138')
    db = client.get_database('fbta_20200112_1305')
    db = client.get_database('fbta_20200202_1816') # full 02-2563
    collection = db.get_collection('03_post_page')

    pppppp = collection.find({})
    for doc in pppppp:
        bs = Selector(doc.get('source', ''))
        dataft_list: List[Optional[Selector]] = bs.css("div[data-ft]")




        if len(dataft_list) == 0:
            """
            อาทิเช่น note
            """
            # print(dataft_list)
            # print('https://m.facebook.com' + doc['url'])
            if 'story' in doc['url']:
                pass
                # print(doc)
                # print(doc['source'])

        else:
            max_indexx = [len(x.attrib['data-ft']) for x in dataft_list]
            max_index = max_indexx.index(max(max_indexx))
            dataparse(dataft_list[max_index].attrib['data-ft'], doc)
