from pymongo import MongoClient



db_name = 'fbta_20200202_1816'

client = MongoClient()
db = client.get_database(db_name)
coll = db.get_collection('03_post_page')

key =  {'img-count':{'$exists':True}}
coll.remove(key)