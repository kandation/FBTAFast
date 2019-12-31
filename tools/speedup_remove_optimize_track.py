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

    docs_post = coll_card.count_documents({'main-link': '#'})
    print(f'Please Wait {docs_post}')
    k = coll_card.update_many({'next-downloaded':True}, {'$unset':{'next-downloaded':True}})
    print(f'Fin remove NextDownload= match{k.matched_count} mod={k.modified_count}')

    docs_post = coll_card.count_documents({'skip-donotcare': True})
    print(f'Start Remove DontCare {docs_post}')
    k = coll_card.update_many({'skip-donotcare': True}, {'$unset': {'skip-donotcare':1}})
    print(f'Fin remove NextDownload match={k.matched_count} mod={k.modified_count}')

