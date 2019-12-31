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
                   'posted', 'untagged'
                   ]
    for hm in header_mini:
        if hm in text:
            return hm
    return '!!!UNKNOWTAG:' + text if len(text.strip()) > 0 else ''


def parsing_mainlink(card):
    """
        # Mainlink Search
    """
    alink = card.xpath('.//div/a')
    alink_main = alink[0].attrib.get('href', '#')
    return html_url.unescape(alink_main)


def parsing_header(card):
    header = card.xpath('.//h3[not(h3)]')

    header_full_text_orginal = ''.join(header.xpath('.//text()').getall())
    header_full_text = header_full_text_orginal
    header_links: List[Optional[Selector]] = header.xpath('.//a')

    param = []

    for header_link in header_links:
        header_link_text = remove_tags(header_link.get())
        header_full_text = header_full_text.replace(header_link_text, '')

        param.append({
            'text': header_link_text,
            'link': html_url.unescape(header_link.attrib.get('href', ''))
        })

    header_full_text = header_full_text.replace("'s", '')
    header_full_text = header_full_text.replace(".", '')

    simplify_header_text = mini_header(header_full_text)

    if '-1' in simplify_header_text and len(header_full_text.strip()):
        with open(f'header_mini_{time_start.strftime("%Y%m%d_%H%M%S")}.txt', mode='a') as fo:
            fo.write(header_full_text + '\n')

    # Note:: if len(header_text) <= 0
    # ประเภท ไม่มีหัวข้อ// มักจะเป็นการโพสด้วยตัวเอง // หรือโพสรูปเปล่าๆ ไม่ได้มีคอมเม้นอะไรเลย/ สามารถใช้นับโสตัวเองได้

    header_return = {
        'type': 'no-header' if len(header_full_text_orginal.strip()) == 0 else 'ok',
        'simplify': simplify_header_text,
        'fulltext': header_full_text_orginal,
        'links': param,
    }

    return header_return


def parsing_content(card, doc_id):
    h4_content = card.css('h4')
    privacy = []
    content_html = ''
    content_text = ''
    thinking_type = 'normal'

    if len(h4_content) == 1:
        privacy = h4_content.xpath('.//*/text()').getall()
        if len(privacy) == 0:
            # แสดงว่าเป็นโพสประเภท โพสที่ถูกลบ คอมเม้นที่ไม่ได้ขึ้นสถานะส่วนตัว การเริ่มเป็นเพื่อน การเข้ากลุ่ม โดนซ่อนโพส
            thinking_type = 'type-1'


    elif len(h4_content) == 2:
        privacy = h4_content[1].xpath('.//*/text()').getall()
        content_html = html_url.unescape(h4_content[0].get())
        content_text = ''.join(h4_content[0].xpath('.//*/text()').getall())
        if len(privacy) == 0:
            # ส่วนใหญ่จะเป็นการ like comment
            thinking_type = 'type-2'

    else:
        with open(f'content_error_{time_start.strftime("%Y%m%d_%H%M%S")}.txt', mode='a') as fo:
            fo.write(str(doc_id) + '\n')

    clean_privacy = []
    for privacy_text in privacy:
        cc = str(privacy_text).strip()
        if len(cc) > 1:
            clean_privacy.append(cc)

    content_return = {
        'privacy': clean_privacy,
        'content-text': content_text,
        'content-html': content_html,
        'type-think': thinking_type,
    }

    return content_return


def tlstory_get_date(tlstory):
    tlmonth, tlday, tlyear = tlstory.attrib.get('id').split('_')[1:]
    tlunits_date = [int('20' + str(tlyear)), int(tlmonth), int(tlday)]
    units_datetime = datetime.datetime(tlunits_date[0], tlunits_date[1], tlunits_date[2])
    return units_datetime.timestamp()


if __name__ == '__main__':
    time_start = datetime.datetime.now()
    data_cid = 0
    client = MongoClient()
    # db = client.get_database('fbta_20190827_1544')
    # db = client.get_database('fbta_20190619_0031')
    # db = client.get_database('fbta_20190827_2027')
    db = client.get_database('fbta_20191111_1236')
    collection = db.get_collection('01_activity_page')

    q_docs = collection.find()
    print(q_docs.count())

    for doc in q_docs:
        bs = Selector(doc.get('source', ''))
        tlunits: List[Optional[Selector]] = bs.css("div[id^=tlRecentStories_]")

        for tlstory in tlunits:
            unit_timestamp = tlstory_get_date(tlstory)

            cards: List[Optional[Selector]] = tlstory.xpath('./div/div')

            for card in cards:
                mainlink = parsing_mainlink(card)
                headers = parsing_header(card)
                contents = parsing_content(card, doc['_id'])

                data = {
                    'cid': data_cid,
                    'time-process': int(datetime.datetime.utcnow().timestamp()),
                    'time-timeline': int(unit_timestamp),
                    'ref-id': doc.get('_id', ''),
                    'main-link': mainlink,
                    'header': headers,
                    'contents': contents,
                    'raw': html_url.unescape(card.get())
                }
                data_cid += 1

                print(data)
