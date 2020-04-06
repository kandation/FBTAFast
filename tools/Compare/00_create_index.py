import pymongo
from pymongo import MongoClient
from time import time

db_name = 'fbta_20200404_1328'
client = MongoClient()
db = client.get_database(db_name)

collection_tlcard = db.get_collection('02_card_page')
collection_story = db.get_collection('03_post_page')


collection_tlcard.create_index([("main-link", pymongo.DESCENDING)])
collection_story.create_index([("url", pymongo.DESCENDING)])

