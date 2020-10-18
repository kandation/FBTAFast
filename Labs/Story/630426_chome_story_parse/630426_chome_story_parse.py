import re as regex
import pathlib

from parsel import Selector
from pymongo import MongoClient

db_name = 'fbta_20200426_0205'
client = MongoClient()
db = client.get_database(db_name)
collection = db.get_collection('03_post_page')

docs = collection.find()

for doc in docs:
    # print(dict(doc).keys())
    ref = db.dereference(doc.get('history'))
    header_sim = ref.get('header').get('simplify')
    header_sim_type = ref.get('header').get('type')
    ab = ['shared', 'ok', 'added', 'likes', 'commented']
    # if header_sim_type == 'ok' and header_sim not in ab:
    #     print(ref)
    #     # print(doc)
    #     # print()

    source = doc.get('source')
    PATT = '\<\!\-\- (.+) \-\-\>'
    xx = regex.search(PATT, source)
    if xx is None:
        """
        : Cannot find html comment 
        : https://m.facebook.com/story.php?story_fbid=3320556414644170&id=100000695314425
        """
        print(doc.get('url'))

    else:
        dir = pathlib.Path(__file__).parent.absolute()

        # exit()
        with open(f'{dir}/story_chome.html', mode='w') as fo:
            fo.write(source)
        print(source)
        input()

    # sel = Selector(source)

    # print(source)
    # exit()
