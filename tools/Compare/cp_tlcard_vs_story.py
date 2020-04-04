from pymongo import MongoClient
from time import time

db_name = 'fbta_20200404_1328'
client = MongoClient()
db = client.get_database(db_name)

collection_tlcard = db.get_collection('02_card_page')
collection_story = db.get_collection('03_post_page')
num_tl = collection_tlcard.estimated_document_count()
num_story = collection_story.estimated_document_count()
num_no_link = collection_tlcard.count_documents({'main-link': '#'})
num_diff = num_tl - num_story
print(
    f'tl={num_tl} story={num_story} (def={num_diff}) {"==" if num_diff == num_no_link else "!="} (no-url={num_no_link})')
analysis_code = 'No error' if num_diff == num_no_link else 'maybe not complete'
print('>> ', analysis_code)
docs_tl = collection_tlcard.find().skip(0)

print('Find Duplicate URL')
cc = 0
start_time = time()
for doc_tl in docs_tl:
    if cc % 1000 == 0:
        print('.', end=str(cc))
    cc += 1
    if doc_tl.get('main-link') != '#':
        docs_story = collection_story.count_documents({'url': doc_tl.get('main-link')})
        if docs_story <=0 :
            pass
            # print(docs_story)
            # print(doc_tl)
            print(collection_story.find_one({'url': doc_tl.get('main-link')}))
            print('-' * 50)
print()
print(f'\nDocsLen={cc}')
print(f'Time= {(time() - start_time) / 60}')
