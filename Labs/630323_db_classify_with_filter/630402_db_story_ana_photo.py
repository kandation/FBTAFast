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

db_name = 'fbta_20200202_1816'

if __name__ == '__main__':
    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('03_post_page')

    docs_post = collection.find().sort([['_id', -1]])

    for doc in docs_post:
        m_source = doc.get('source', '')
        bs = Selector(m_source)

        data_pp = {
            'story-info': {
                'is-story': False,

            },
            'link-info': {
                'type': 'n/a',
                'optional': []
            }

        }
        # This content isn't available right now
        story_block = bs.css('div#m_story_permalink_view')

        if story_block:
            """ ใช้ตรวจสอบว่าเป็น story ๗ริงไหม  ถ้ามีบล๊อกนี้แสดงว่าเป็น"""
            m_source_only_content = story_block.css('div > div')

            px = m_source_only_content[0].xpath('descendant-or-self::a/img[@width>20]/parent::a')
            vx = m_source_only_content[0].xpath("descendant-or-self::div/img[not(@width) or @width>20]/../../../a")
            lx = m_source_only_content[0].css('td > img')
            # เอาเฉพาะลิงก์ที่มีรูปก็พอละ ส่วนลิงก์ไม่มีรูปคงใช้ data-ft ทายเอา แต่ก็คงไม่สนใจมาก ไป  nl[ จาก header  ดีกว่า

            lenght = [len(px), len(vx), len(lx)]

            link_type = 'other'
            link_optional = []

            if lenght[0]:
                # พวกที่เป็นอัลบัมยังต้องไปตรวจสอบอีกว่าเป็นวีดีโอหรือไม่ แต่ทำให้ขั้นตอนหาอัลบัมเลยก็ได้
                link_optional = px.xpath('@href').getall()
                link_type = 'photo' if lenght[0] == 1 else 'album'

            if lenght[1] == 1:
                link_type = 'video'
                video_url = unquote(vx.xpath('@href').get())
                img_url = unquote(vx.css('img').attrib['src'])
                link_optional = [video_url, img_url]

            if lenght[2]:
                # มัน detect ได้มากกว่านี้ แต่ไว้ค่อยทำ (ใช้แบบ web จะได้ภาพใหญ่กว่า)
                link_type = 'link' if lenght[2] == 1 else 'link-cluster'

            data_pp['story-info']['is-story'] = True
            data_pp['link-info']['type'] = link_type
            data_pp['link-info']['optional'] = link_optional

        else:
            """ถ้าไม่มีแสดงว่าไม่เป็น อาจจะเป็นพวก Note, รูปภาพที่อัพโหลดเอง, คอมเม้นที่อยู่ในภาพเดี่ยวสมัยโบราณ"""
            pass
            # print(f"{fb_url_m}/{doc.get('url')}")

        collection.update_one({'_id': doc.get('_id')}, {'$set': data_pp})
