import json
import xml.etree.ElementTree
from pprint import pprint
from typing import List, Optional

from parsel import Selector
from pymongo import MongoClient
from lxml import etree, html
import html as html_url
from bson.objectid import ObjectId

import datetime

import re


def remove_tags(text):
    return html_url.unescape(re.compile(r'<[^>]+>').sub('', text))


def hprint(h):
    document_root = html.fromstring(h)
    print(etree.tostring(document_root, encoding='unicode', pretty_print=True))


def mini_header(text):
    header_mini = ['shared', 'posted in', 'via', 'reviewed', 'subscribed', 'was at', 'uploaded', 'going to',
                   'likes', 'commented', 'replied', 'reacted', 'liked', 'was tagged', 'voted', 'saved', 'updated',
                   'was live', 'approved', 'published', 'using', 'edited', 'changed', 'replied', 'wrote on', 'followed',
                   'mentioned', 'became', 'is with', 'was with', 'is at', 'sent',
                   'poked', 'added', 'feeling', 'created', 'played', 'breeding', 'evolved', 'took', 'earned',
                   'new high score',
                   'celebrating', 'solved', 'interested', 'watching', 'was playing', 'searched', 'watched', 'removed',
                    'posted','untagged'
                   ]
    for hm in header_mini:
        if hm in text:
            return hm
    return '!!!UNKNOWTAG:'+text


if __name__ == '__main__':
    time_start = datetime.datetime.now()
    client = MongoClient()
    # db = client.get_database('fbta_20190827_1544')
    # db = client.get_database('fbta_20190619_0031')
    db = client.get_database('fbta_20190827_2027')
    collection = db.get_collection('01_activity_page')

    # q_docs = collection.find({'_id': ObjectId("5d64edbeb0e15911283d6710")})
    q_docs = collection.find()

    print(q_docs.count())
    for doc in q_docs:

        bs = Selector(doc.get('source', ''))
        # '//id[starts-with(text(),'Annotations')]'
        # tlunits = bs.xpath("//div[@id and contains(@id,'tlUnit_')]")
        # tlunits = bs.xpath("//div[@id and contains(@id,'tlRecentStories_')]")
        # for tlunit in tlunits:
        #     print(tlunit)

        # tlrecent: List[Optional[Selector]] = bs.css("div[@id and contains(@id,'tlRecentStories_')]")
        #     print(tlrecent)
        # exit()
        # tlrecent = [tlrecent[1]]
        tlunits: List[Optional[Selector]] = bs.css("div[id^=tlRecentStories_]")
        for tlstory in tlunits:
            # hprint(tlunits[0].get())

            cards: List[Optional[Selector]] = tlstory.xpath('./div/div')
            cards = cards
            for card in cards:
                # TODO FIND MAIN LINK
                # hprint(card.get())

                alink = card.xpath('.//div/a')
                alink_main = alink[0].attrib.get('href','#')
                if alink_main[0] not in ['#','/']:
                    print(html_url.unescape(alink_main))

                # header = card.css('h3')
                header = card.xpath('.//h3[not(h3)]')
                kk = header.xpath('(.//*)').getall()
                # print(header.getall())
                # print(kk)
                # input()
                header_full_text = ''.join(header.xpath('.//text()').getall())
                header_attrb_text = header.xpath('.//*/text()').getall()
                header_attrb_text_a = header.xpath('.//a/text()').getall()
                header_attrb_text_aaa: List[Optional[Selector]] = header.xpath('.//a')
                header_attrb_text_ahref = header.xpath('.//a/@href').getall()
                # if header_attrb_text != header_attrb_text_a:
                # อย่าตัดด้วย attrb/ text กากมาก ใ้ห get a  แล้วจัดการดีกว่า

                param = []

                for ppp in header_attrb_text_aaa:
                    header_text_link = remove_tags(ppp.get())
                    header_full_text = header_full_text.replace(header_text_link, '')

                    param.append({
                        'text': header_text_link,
                        'link': ppp.attrib.get('href')
                    })
                header_full_text = header_full_text.replace("'s", '')
                header_full_text = header_full_text.replace(".", '')
                mmm = mini_header(header_full_text)
                if '!!!' in mmm and len(header_full_text.strip()):
                    print(mmm, param, header)
                    with open(f'header_mini_{time_start.strftime("%Y%m%d_%H%M%S")}.txt', mode='a') as fo:
                        fo.write(header_full_text + '\n')

                # print(header_attrb_text_aaa)
                # TODO SPliter HEADER

                # print(header_text)

                # for h in header:
                #     print(h.get())
                # print(header)

                h4_content = card.css('h4')

                # if len(header_text) < 15:
                #     # ประเภท ไม่มีหัวข้อ// มักจะเป็นการโพสด้วยตัวเอง // หรือโพสรูปเปล่าๆ ไม่ได้มีคอมเม้นอะไรเลย/ สามารถใช้นับโสตัวเองได้
                #     print('---------')
                #     print(h4_content.get())
                #     print(doc.get('current-url'))
                #     print('---------')

                # print(privacy)
                if len(h4_content) == 1:
                    pass
                    privacy = h4_content.xpath('.//*/text()').getall()
                    # print(header_text,privacy)
                    # if not len(privacy):
                    #     will_be_del = True
                    #     # มีทั้งโพสที่ถูกลบ คอมเม้นที่ไม่ได้ขึ้นสถานะส่วนตัว การเริ่มเป็นเพื่อน การเข้ากลุ่ม โดนซ่อนโพส
                    #     print('------',header_text,doc.get('current-url'))
                elif len(h4_content) == 2:
                    privacy = h4_content[1].xpath('.//*/text()').getall()
                    content_html = html_url.unescape(h4_content[0].get())
                    content_text = ''.join(h4_content[0].xpath('.//*/text()').getall())
                    # print(header_text,privacy)
                    # if not len(privacy):
                    #     will_be_del = True
                    #     # มส่วนใหญ่จะเป็นการ like comment
                    #     print('------',header_text,doc.get('current-url'))

                else:
                    # print(card.get())
                    print('************', len(h4_content), '\n')

                    # for aa in cards.getall():
                    #     print(aa)
                    # print(doc['_id'])
                    # print(doc.get('current-url'))
                    # exit()
            # print()

            # print()
            # input('>> Enter')
