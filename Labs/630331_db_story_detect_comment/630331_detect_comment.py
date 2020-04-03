import json, os
from pprint import pprint
from typing import List, Optional

from parsel import Selector
from pymongo import MongoClient


fb_url_m = 'https://m.facebook.com/'
fb_url_w = 'https://www.facebook.com/'

db_name = 'fbta_20200331_2306'



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
    """
    ส่วนใหญ่ url ที่อยู่ในรูปแบบ like comment จะมี url 
    /story.php?story_fbid=2779266055524671&id=285341701583798&comment_id=2779292498855360
    ซึ่งสามารถหาได้ทาง comment_id=2779292498855360 และ
    div class="dz" id="2779292498855360" แล้วหา photo โง่ๆได้เลย 
    
     บ้างอย่างต้องเข้าผ่าน m.facebook WTF มากๆ
     .com/comment/replies/?ctoken=28091461...
     """

    client = MongoClient()
    db = client.get_database(db_name)
    collection = db.get_collection('03_post_page')

    docs_post = collection.find()


    for doc in docs_post:
        m_source = doc.get('url')
        #/story.php?story_fbid=2779266055524671&id=285341701583798&comment_id=2779292498855360
        if 'c' in m_source:
            print(doc)
            print(m_source)
