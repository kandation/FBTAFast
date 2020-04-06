import time

from pymongo import MongoClient

cilent = MongoClient()
db = cilent.get_database('fbta_20200405_0314')
coll = db.get_collection('99_photos_tank')

key = {'downloaded-recheck': {'$exists': False}}
key_clear = {'downloaded-recheck': {'$exists': True}}

f = coll.find(key_clear)
print(f.count())
x = coll.update_many(key_clear, {'$unset': {'downloaded-recheck': True}})
print(x)

f = coll.find(key_clear)
print(f.count())

# f = coll.find(key).skip(0).limit(5000)
# i = 0
#
# suma = 0
# while True:
#     try:
#         k = f.next()
#         coll.update_one({'_id': k.get('_id')}, {'$set': {'downloaded-recheck': True}})
#         i+=1
#     except StopIteration:
#         print(i)
#         suma += i
#         i=0
#         f = coll.find(key).skip(0).limit(5000)
#         e = f.count()
#         if not e:
#             break
# print(suma, coll.estimated_document_count())

start = time.time()
# z = coll.find(key_clear).count()
z = coll.count_documents(key_clear, limit=1)
# z= coll.estimated_document_count()
print(z, time.time() - start)
