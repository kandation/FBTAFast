db_name = 'fbta_20200423_0244'

from parsel import Selector
from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient()
    db = client.get_database(db_name)
    coll_photo = db.get_collection('98_album_no_duplicate')

    docs_post = coll_photo.find()


    photos_list = {}
    counter = 0

    for doc in docs_post:
        source = doc.get('photo-cluster')[0].get('source')
        sel = Selector(source)
        title = sel.css('title')
        if 'This Feature Right Now' in title.get():
            print(doc.get('photo-cluster')[0].get('url'))
        # print(.get('success'))