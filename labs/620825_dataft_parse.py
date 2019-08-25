from typing import List, Optional

from parsel import Selector
from pymongo import MongoClient

client = MongoClient()
db = client.get_database('fbta_20190824_1839')
collection = db.get_collection('03_post_page')

pppppp = collection.find({})
for doc in pppppp:
    bs = Selector(doc['source'])
    dataft_list: List[Optional[Selector]] = bs.css("div[data-ft]")
    if len(dataft_list) == 0:
        print('https://m.facebook.com'+doc['url'])
        if 'story' in  doc['url']:
            print(doc['source'])
    else:
        max_indexx = [len(x.attrib['data-ft']) for x in dataft_list]
        max_index = max_indexx.index(max(max_indexx))

