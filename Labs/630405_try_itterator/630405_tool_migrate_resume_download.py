import time

from pymongo import MongoClient

cilent = MongoClient()
db = cilent.get_database('fbta_20200404_1650')
coll = db.get_collection('99_photos_tank')

key = {'downloaded-recheck': {'$exists': False}}
key_clear = {'downloaded-recheck': {'$exists': True}}
key_downloaded = {'downloaded': {'$exists': True}}

f = coll.update_many(key_downloaded, {'$set': {'downloaded-recheck': True}})
