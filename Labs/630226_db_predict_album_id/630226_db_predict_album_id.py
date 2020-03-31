from pymongo import MongoClient

if __name__ == '__main__':
    db_name = 'fbta_20200202_1816'

    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('03_post_page')

    key = {'dataft.dataft-type': {'$exists': True}}
    docs_album = collection.find(key)