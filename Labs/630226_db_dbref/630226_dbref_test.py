from pymongo import MongoClient

db_name = 'fbta_20200202_1816'
client = MongoClient()
db = client.get_database(db_name)
collection = db.get_collection('03_post_page')

docs = collection.find()


for doc in docs:
    ref = db.dereference(doc.get('history'))
    header_sim = ref.get('header').get('simplify')
    header_sim_type = ref.get('header').get('type')
    ab = ['shared', 'ok', 'added','likes','commented']
    if header_sim_type == 'ok' and header_sim not in ab:
        print(ref)
        # print(doc)
        # print()