"""
ไฟล์นี้ทำหน้าที่ค้นหาชื่อ Title ของเพจ ที่ต่างจากพวก
ใช้ในการหาร Facebook Error pages
"""
from pymongo import MongoClient
import re as regex

if __name__ == '__main__':
    client = MongoClient()
    except_db_global_list = ['admin', 'config', 'local']


    except_db_list = ['fbta_20200404_1328']

    PATTERN_TITLE = "<title>(.+)</title>"

    ignore_case = ['Comments']
    focus_case = ['http']

    fb_url = 'https://www.facebook.com/'

    for db_name in client.list_database_names():
        db = client.get_database(db_name)
        coll = db.get_collection('03_post_page')
        # num_card = coll_card.estimated_document_count()
        docs = coll.find({})
        for doc in docs:
            source = doc.get('source')
            result = regex.search(PATTERN_TITLE, source)
            if result:
                text = ''.join(result.groups())

                if text not in ignore_case:
                    if 'Error' in text:
                        print(f'{fb_url}{doc.get("url")}',text[:50])
                        print(source,end='\n\n')


