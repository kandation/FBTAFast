import json, os
from pprint import pprint
from typing import List, Optional

from parsel import Selector
from pymongo import MongoClient

import m_630323_01_style as m_style

fb_url_m = 'https://m.facebook.com/'
fb_url_w = 'https://www.facebook.com/'

db_name = 'fbta_20200202_1816'


def write_new_json(new_onehot):
    with open(f'{os.path.dirname(__file__)}/onehot.json', mode='w', encoding='utf8') as fo:
        fo.write(json.dumps(new_onehot, ensure_ascii=False))


# def nlp_clean_text(txt):
#     for t in txt:
#         t =

def kkkkk(dbref):
    ref = db.dereference(dbref)
    header_sim = ref.get('header').get('simplify')
    header_sim_type = ref.get('header').get('type')
    ab = ['shared', 'ok', 'added', 'likes', 'commented']
    hd = ref.get('header')
    import re
    PATT = '^(.+)likes(.+)album'
    kas = re.match(PATT, hd.get('fulltext'))
    print(hd, 'https://m.facebook.com/'+ref.get('main-link'))
    if kas:
        print([x.strip() for x in kas.groups()])
    # if header_sim_type == 'ok' and header_sim not in ab:
    #     print(ref)


if __name__ == '__main__':
    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('03_post_page')

    docs_post = collection.find()

    dataft_onehot_key = ['mf_story_key', 'top_level_post_id', 'tl_objid', 'throwback_story_fbid', 'story_location',
                         'story_attachment_style', 'tn', 'content_owner_id_new', 'page_id', 'page_insights', 'photo_id',
                         'tagged_locations', 'attached_story_attachment_style', 'photo_attachments_list',
                         'original_content_id', 'original_content_owner_id', 'call_to_action_type', 'ref', 'qid', 'src',
                         'view_time', 'filter', 'og_action_id', 'group_id', 'text_formatting', 'media_with_effects_id',
                         'profile_picture_overlay_owner', 'profile_picture_overlay_id']

    with open(f'{os.path.dirname(__file__)}/onehot.json', mode='r', encoding='utf8') as fo:
        onehot_instruct = json.loads(fo.read())

    import copy

    onehot_clone = copy.deepcopy(onehot_instruct)

    for doc in docs_post:
        m_source = doc.get('source')
        bs = Selector(doc.get('source', ''))
        dataft_list: List[Optional[Selector]] = bs.css("div[data-ft]")

        if len(dataft_list) != 0:
            dataft_str = m_style.find_max_dataft(dataft_list)
            st = m_style.dataparse(dataft_str, doc)

            # if st == 'photo':
            #     #  กรณีที่เป็นรูปภาพ 100%  จะมีแท็ photo_id
            #     datft_argument = ['0' for _ in range(len(dataft_onehot_key))]
            #     js = json.loads(dataft_str, encoding='utf8')
            #     for key in js:
            #         if key in dataft_onehot_key:
            #             datft_argument[dataft_onehot_key.index(key)] = '1'
            #
            #     type_arg = ''.join(datft_argument)
            #     if onehot_instruct[type_arg][1] != '':
            #         if type_arg[10]=='1':
            #             print(onehot_instruct[type_arg], js)
            #     #     ins = input('>>')
            #     #     if ins != '':
            #     #         onehot_instruct[type_arg][1] = ins
            #     #         write_new_json(onehot_instruct)
            #     # # print(onehot_instruct[type_arg])

            if st == 'album':
                datft_argument = ['0' for _ in range(len(dataft_onehot_key))]
                js = json.loads(dataft_str, encoding='utf8')
                for key in js:
                    if key in dataft_onehot_key:
                        datft_argument[dataft_onehot_key.index(key)] = '1'

                type_arg = ''.join(datft_argument)
                if onehot_instruct[type_arg][1] == '':
                    ผ

                    ref = db.dereference(doc.get('history'))
                    simplify = ref.get('header').get('simplify')


                    if simplify == '':
                        kkkkk(doc.get('history'))
                        print('beshare')
                        print(onehot_instruct[type_arg], js)
                        print('-----------')
                        # if type_arg[10] == '1':
                        #     print(onehot_instruct[type_arg], js)
                #     ins = input('>>')
                #     if ins != '':
                #         onehot_instruct[type_arg][1] = ins
                #         write_new_json(onehot_instruct)
                # # print(onehot_instruct[type_arg])

    print(onehot_instruct)
    write_new_json(onehot_instruct)
