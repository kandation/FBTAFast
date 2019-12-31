"""
Track loaded to first table
"""
import time

from pymongo import MongoClient

name_db = 'fbta_20191114_1901'
# name_db = 'Test621114'
name_coll_card = '02_card_page'
name_coll_post = '03_post_page'


if __name__ == '__main__':

    client = MongoClient()
    db = client.get_database(name_db)
    coll_card = db.get_collection(name_coll_card)
    coll_post = db.get_collection(name_coll_post)

    # for i in range(100):
    #     coll_post.insert_one({'_id':i})

    docs_post = coll_post.find()
    cc0 = 0

    time_start0 = time.time()
    while True:
        try:
            nx = docs_post.next()
            nxp = docs_post
            print(nxp)
            print(nx)
            exit()
            # print(nx.get('_id'))
            cc0 += 1
        except StopIteration as e:
            print(e)
            break
    time_stop0 = time.time()

    time_start1 = time.time()
    cc = 0
    docs_post.rewind()
    for doc in docs_post:
        # print(doc)
        # print(doc.get('_id'))
        # nx = docs_post.rewind()
        # print(nx.get('_id'))
        cc+=1
    print('cc=', cc0)
    print(f'stop={time_stop0 - time_start0}')
    print('cc=',cc)
    print(f'stop={time.time()-time_start1}')

