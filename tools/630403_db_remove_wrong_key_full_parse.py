from pymongo import MongoClient

db_name = 'fbta_20200202_1816'

# อิสัส มันลบทั้งหมดเลยนะ ระวังด้วย

client = MongoClient()
db = client.get_database(db_name)
coll = db.get_collection('03_post_page')

key =  {'link-info':{'$exists':True}}
coll.remove(key)
