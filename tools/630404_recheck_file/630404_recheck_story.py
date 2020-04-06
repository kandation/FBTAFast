db_name = 'fbta_20200404_1328'

from parsel import Selector
from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient()
    db = client.get_database(db_name)
    coll_photo = db.get_collection('03')

    docs_post = coll_photo.find()


    photos_list = {}
    counter = 0

    for doc in docs_post:
        if not doc.get('downloaded'):
            print(doc)
        # print(.get('success'))