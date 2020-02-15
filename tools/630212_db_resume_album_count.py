from pymongo import MongoClient



name_db = 'fbta_20200202_1816'
name_coll_post = '03_post_page'
name_coll_album = '05_album_count'


if __name__ == '__main__':
    client = MongoClient()
    db = client.get_database(name_db)
    coll_post = db.get_collection(name_coll_post)
    coll_album = db.get_collection(name_coll_album)

    # docs_post = coll_post.find({'dataft.dataft-type': {'$exists': True}})
    docs_post = coll_album.find()
    # print(docs_post.count())
    for doc in docs_post:
        print(doc.get('url'), doc.get('history'))
        coll_post.update_one({'_id':doc.get('history')}, {'$set':{'album-next-downloaded':True}})
