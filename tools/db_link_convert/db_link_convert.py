from pymongo import MongoClient
from urllib import parse


'''
@docs: ไฟล์นี้ทำหน้าที่ค้นหา record ที่มี main-link เหมือนกัน และทำการแปลงกลับในทิศทางเดียว
Docs_A --[1:m]--> Docs_A
'''

db_name = 'fbta_20200112_1305'
client = MongoClient()
db = client.get_database(db_name)

collection_tlcard = db.get_collection('02_card_page')
collection_story = db.get_collection('03_post_page')

docs_tl = collection_tlcard.find()

print(collection_tlcard.estimated_document_count())

for doc in docs_tl:
    pe = str(doc.get('main-link')).split('?')[-1]
    url = parse.parse_qsl(pe)
    s = {k: v for k, v in url}
    # if 'substory_index' not in s:
    #     print(doc.get('main-link'))
    if 'story' not in doc.get('main-link'):
        print(doc.get('main-link'))
        print(doc,'\n')
