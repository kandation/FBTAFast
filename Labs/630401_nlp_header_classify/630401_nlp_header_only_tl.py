import json, os
from pprint import pprint
from typing import List, Optional

from parsel import Selector
from pymongo import MongoClient
import re as regex

fb_url_m = 'https://m.facebook.com/'
fb_url_w = 'https://www.facebook.com/'

db_name = 'fbta_20200412_1808'


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
    collection = db.get_collection('02_card_page')

    docs_post = collection.find()

    PATT_LIST = {
        'became': {'label': ['own', 'who'], 'pattern': '(.+) became friends with (.+).', 'own': 'me',
                   'target': 'other'},
        'write': {'label': ['who', 'place'], 'pattern': '(.+) wrote on (.+).', 'own': 'other', 'target': 'me'},
        'like': {'label': ['own', 'object'], 'pattern': '(.+) likes (.+).', 'own': 'other', 'target': 'other'},
        'like-other': {'label': ['own', 'who', 'object'], 'pattern': '(.+) liked (.+)\'s (.+).', 'own': 'other',
                       'target': 'other'},
        'updated': {'label': ['own', 'prep', 'object'], 'pattern': '(.+) updated (him|her|them) (.+).',
                    'own': 'me', 'target': 'me'},
        'changed': {'label': ['own', 'prep', 'objective', 'new-object'],
                    'pattern': '(.+) changed (him|her|them) (.+) to (.+).', 'own': 'me',
                    'target': 'me'},
        'added': {'label': ['own', 'object'], 'pattern': '(.+) added (.+).', 'own': 'me', 'target': 'me'},
        'added-place': {'label': ['own', 'object', 'place'], 'pattern': '(.+) added (.+) — at (.+).', 'own': 'me',
                        'target': 'me'},
        'added-with': {'label': ['own', 'object', 'who'], 'pattern': '(.+) added (.+) — with (.+).', 'own': 'me',
                       'target': 'me'},
        'like-other-on': {'label': ['own', 'who', 'object', 'where'], 'pattern': "(.+) likes (.+)'s (.+) on (.+).",
                          'own': 'me', 'target': 'other'},
        'tagged': {'label': ['own'], 'pattern': "(.+) was tagged."},
        'using': {'label': ['own', 'object'], 'pattern': "(.+) is now using Facebook in (.+).", 'own': 'me',
                  'target': 'na'},
        'commented': {'label': ['own', 'who'], 'pattern': "(.+) commented on (.+)'s post.", 'own': 'me',
                      'target': 'other'},
        'edited': {'label': ['own', 'prep', 'object'], 'pattern': "(.+) edited (him|her|them) Looking For, (.+)",
                   'own': 'me',
                   'target': 'me'},
        'shared': {'label': ['own', 'object'], 'pattern': "(.+) shared a (.+).",
                   'own': 'me',
                   'target': 'other'},
    }

    info = {
        'me': 'fadehara',
        'ignor':[
            'khwanchai.sil', 'quint.tom.1','Jirutchaya.Janthayuen','jaideejung007','au.z.huahin','tiemtud','choy.kanitsak','sukanya.tongheang'
        ]
    }

    debug_case = ['like-other']
    for doc in docs_post:

        fulltext = doc.get('header').get('fulltext')
        # if fulltext == '':
        #     print('https://m.facebook.com'+doc.get('main-link'))
        #     print(doc)

        sr = None
        print(doc.get('header').get('links'))
        for patt_key in PATT_LIST:
            PATT = PATT_LIST[patt_key].get('pattern')
            search = regex.fullmatch(PATT, fulltext)
            if search:
                sr = [search.groups(), patt_key]

        if sr:
            print(sr)
            if sr[1] in debug_case:
                print(doc.get('header'))
        else:
            print(doc.get('header'))
        print('---------')

        # m_source = doc.get('source')
        # bs = Selector(doc.get('source', ''))
        # dataft_list: List[Optional[Selector]] = bs.css("div[data-ft]")
        # ref = db.dereference(doc.get('history'))
        # simplify = ref.get('header').get('simplify')
        # print(ref.get('header').get('fulltext'))
