from pymongo import MongoClient

db_name = 'fbta_20200112_1305'
client = MongoClient()
db = client.get_database(db_name)

collection_tlcard = db.get_collection('02_card_page')
nn = ['album', 'post', 'photo']
docs_tl = collection_tlcard.find()
for docs in docs_tl:
    k = docs.get('header').get('fulltext')
    ss = [(ns in k) for ns in nn]
    if not any(ss):
        print(docs.get('header').get('fulltext'), '-----', docs.get('header').get('simplify'))
        print(docs.get('header').get('links'))
