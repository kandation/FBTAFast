import json, os
from pprint import pprint
from typing import List, Optional

from parsel import Selector
from pymongo import MongoClient

fb_url_m = 'https://m.facebook.com/'
fb_url_w = 'https://www.facebook.com/'

db_name = 'fbta_20200202_1816'


def write_new_json(new_onehot):
    with open(f'{os.path.dirname(__file__)}/onehot.json', mode='w', encoding='utf8') as fo:
        fo.write(json.dumps(new_onehot, ensure_ascii=False))


def kkkkk(dbref):
    ref = db.dereference(dbref)
    header_sim = ref.get('header').get('simplify')
    header_sim_type = ref.get('header').get('type')
    ab = ['shared', 'ok', 'added', 'likes', 'commented']
    hd = ref.get('header')
    import re
    PATT = '^(.+)likes(.+)album'
    kas = re.match(PATT, hd.get('fulltext'))
    print(hd, 'https://m.facebook.com/' + ref.get('main-link'))
    if kas:
        print([x.strip() for x in kas.groups()])
    # if header_sim_type == 'ok' and header_sim not in ab:
    #     print(ref)


if __name__ == '__main__':
    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('03_post_page')

    docs_post = collection.find()

    PATT_LIST = {
        'became': {'label': ['own', 'who'], 'pattern': '(.+) became friends with (.+).', 'own': 'me'},
        'write': {'label': ['who', 'place'], 'pattern': '(.+) wrote on (.+).', 'own': 'other'},
        'like': {'label': ['own', 'target'], 'pattern': '(.+) likes (.+).', 'own': 'other'},
        'updated': {'label': ['own', 'target'], 'pattern': '(.+) updated (.+) status.','own':'me'},
        'changed': {'label': ['own', 'objective', 'new-object'], 'pattern': '(.+) changed (.+) to (.+).','own':'me'},
        'added': {'label': ['own', 'object'], 'pattern': '(.+) added (.+).'},
        'like-other': {'label': ['own', 'who', 'object', 'place'], 'pattern': "(.+) likes (.+)'s (.+) on (.+)."}
    }
    for doc in docs_post:
        m_source = doc.get('source')
        bs = Selector(doc.get('source', ''))
        dataft_list: List[Optional[Selector]] = bs.css("div[data-ft]")
        ref = db.dereference(doc.get('history'))
        simplify = ref.get('header').get('simplify')
        print(ref.get('header'))
