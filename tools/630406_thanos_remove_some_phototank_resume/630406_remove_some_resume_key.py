db_name = 'fbta_20200404_1650'

from parsel import Selector
from pymongo import MongoClient
import random

if __name__ == '__main__':
    """
    Thanos snippet : Remove some "downloaded-recheck" Tag (magic key for resume system)
    """
    client = MongoClient()
    db = client.get_database(db_name)
    coll_photo = db.get_collection('99_photos_tank')

    key = {"downloaded-recheck": {'$exists': True}}
    docs_post = coll_photo.find(key)
    num_coll = docs_post.count()

    counter = 0

    remove_ratio = 0.01

    for doc in docs_post:
        if random.random() <= remove_ratio:
            coll_photo.update_one({'_id': doc.get('_id')}, {'$unset': {"downloaded-recheck": True}})
            counter += 1

    print(f'Remove {counter} from {num_coll} = {(counter + 1) / (num_coll + 1)}')
