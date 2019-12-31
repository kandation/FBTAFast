"""
This tools for make speed for broken link in 02_card_page i.e. `#` link
"""

from pymongo import MongoClient

name_db = 'fbta_20191114_1901'
name_coll_card = '02_card_page'
name_coll_post = '03_post_page'


if __name__ == '__main__':
    client = MongoClient()
    db = client.get_database(name_db)
    coll_card = db.get_collection(name_coll_card)

    docs_post = coll_card.count_documents({'main-link':'#'})
    print(f'Please Wait {docs_post}')
    coll_card.update_many({'main-link':'#'}, {'$set':{'skip-donotcare':True}})
    print()

