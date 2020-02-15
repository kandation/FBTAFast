from fbta_global_database_manager import FBTADBManager

db_name = 'fbta_20200202_1816'
coll_current = '03_post_page'
coll_next = '05_album_count'

dbm = FBTADBManager(db_name, [coll_current, coll_next])

dbm.set_custom_find({'dataft.dataft-type': {'$exists': True}})
docs = dbm.get_current_docs()

for doc in docs:
    print(doc)