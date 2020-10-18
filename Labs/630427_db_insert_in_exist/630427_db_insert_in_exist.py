from bson import ObjectId
from pymongo import MongoClient
import dotty_dict

client = MongoClient()
db = client.get_database('test_database')
coll = db.get_collection('test630427')

data = {
    'outer': 1,
    'pack':
        {'a': 1, 'b':5,'s':9}
}

key = {'_id': ObjectId('5ea6ab96931d88c21febe5a7')}
# print(new_dict)
fx = coll.find_one(key)
# print(fx)
fxp = fx.get('pack')
fxp.update(data.get('pack'))
# print(fx)
coll.update_one(key, {'$set':fx}, upsert=True)
# coll.update(, data)
# coll.insert_one(data)
