"""
Track loaded to first table
"""

from pymongo import MongoClient

name_db = 'fbta_20191114_1901'
name_coll_card = '02_card_page'
name_coll_post = '03_post_page'


if __name__ == '__main__':
    client = MongoClient()
    db = client.get_database(name_db)
    coll_card = db.get_collection(name_coll_card)
    coll_post = db.get_collection(name_coll_post)

    docs_post = coll_post.find()
    for doc in docs_post:
        print(doc.get('url'), doc.get('refer-id'))
        coll_card.update_one({'_id':doc.get('refer-id')}, {'$set':{'next-downloaded':True}})

