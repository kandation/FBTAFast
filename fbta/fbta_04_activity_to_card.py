import re
import time

from fbta.fbta_configs import FBTAConfigs
from fbta.fbta_global_database_manager import FBTADBManager
from fbta.fbta_settings import FBTASettings
from fbta.fbta_log import log

from typing import List, Optional

from parsel import Selector
from lxml import etree, html
import html as html_url

import datetime


class FBTAActivityToCardsNew:
    def __init__(self, settings: FBTASettings, configs: FBTAConfigs):
        list_collection = [
            configs.db_collection_01_page_name,
            configs.db_collection_02_card_name]
        self.db = FBTADBManager(settings.db_name, list_collection, configs.db_collection_stat)

        self.time_start = datetime.datetime.now()
        self.__data_cid = 0

        self.__stat = {
            'insert-fail': 0,
            'insert-success': 0
        }

    def main(self):
        self.__main_run()
        log(f':Act2Card: Finished as {self.__data_cid} cards')
        self.__stat['num-cards'] = self.__data_cid
        self.db.add_stat_to_db('act2card', 'single', self.time_start.timestamp(), time.time(), self.__stat)

    def __main_run(self):
        q_docs = self.db.get_current_docs()
        log(f':Act2Card: Has {q_docs.count()} pages')

        for doc in q_docs:
            bs = Selector(doc.get('source', ''))
            tlunits: List[Optional[Selector]] = bs.css("div[id^=tlRecentStories_]")
            log(f':Act2Card:------------ [{self.__data_cid}] TLUnit = {len(tlunits)} ------------')

            for tlstory in tlunits:
                unit_timestamp = self.tlstory_get_date(tlstory)
                date_tl = datetime.datetime.fromtimestamp(unit_timestamp)
                log(f':Act2Card:\tDate = {date_tl}')

                cards: List[Optional[Selector]] = tlstory.xpath('./div/div')

                for card in cards:
                    mainlink = self.parsing_mainlink(card)
                    headers = self.parsing_header(card)
                    contents = self.parsing_content(card, doc['_id'])

                    data = {
                        'cid': self.__data_cid,
                        'time-process': int(datetime.datetime.utcnow().timestamp()),
                        'time-timeline': int(unit_timestamp),
                        'ref-id': doc.get('_id', ''),
                        'history-cluster-id': doc.get('history-cluster-id', ''),
                        'main-link': mainlink,
                        'header': headers,
                        'contents': contents,
                        'raw': html_url.unescape(card.get()),
                        'raw-docs': {
                            '_id': doc.get('_id', ''),
                            'url': doc.get('current-url', ''),
                            'title': doc.get('title', ''),
                            'created': doc.get('create', ''),
                        }
                    }
                    self.__data_cid += 1

                    if self.__try_insert_db(data):
                        self.__stat['insert-success'] += 1
                        # log(f':Act2Card:\t\tInsert {self.__data_cid} OK')
                    else:
                        self.__stat['insert-fail'] += 1
                        log(f':Act2Card:\t\t> Insert problem {self.__data_cid}')

    def __try_insert_db(self, data):
        try:
            return self.db.next_collection_insert_one(data)
        except Exception as e:
            log('Insert Card Error', e)
            exit()

    def remove_tags(self, text):
        return html_url.unescape(re.compile(r'<[^>]+>').sub('', text))

    @staticmethod
    def hprint(h):
        document_root = html.fromstring(h)
        print(etree.tostring(document_root, encoding='unicode', pretty_print=True))

    @staticmethod
    def mini_header(text):
        header_mini = ['shared', 'posted in', 'via', 'reviewed', 'subscribed', 'was at', 'uploaded', 'going to',
                       'likes', 'commented', 'replied', 'reacted', 'liked', 'was tagged', 'voted', 'saved', 'updated',
                       'was live', 'approved', 'published', 'using', 'edited', 'changed', 'replied', 'wrote on',
                       'followed',
                       'mentioned', 'became', 'is with', 'was with', 'is at', 'sent',
                       'poked', 'added', 'feeling', 'created', 'played', 'breeding', 'evolved', 'took', 'earned',
                       'new high score',
                       'celebrating', 'solved', 'interested', 'watching', 'was playing', 'searched', 'watched',
                       'removed',
                       'posted', 'untagged'
                       ]
        for hm in header_mini:
            if hm in text:
                return hm
        return '!!!UNKNOWTAG:' + text if len(text.strip()) > 0 else ''

    def parsing_mainlink(self, card):
        alink = card.xpath('.//div/a')
        alink_main = alink[0].attrib.get('href', '#')
        return html_url.unescape(alink_main)

    def parsing_header(self, card):
        header = card.xpath('.//h3[not(h3)]')

        header_full_text_orginal = ''.join(header.xpath('.//text()').getall())
        header_full_text = header_full_text_orginal
        header_links: List[Optional[Selector]] = header.xpath('.//a')

        param = []

        for header_link in header_links:
            header_link_text = self.remove_tags(header_link.get())
            header_full_text = header_full_text.replace(header_link_text, '')

            param.append({
                'text': header_link_text,
                'link': html_url.unescape(header_link.attrib.get('href', ''))
            })

        header_full_text = header_full_text.replace("'s", '')
        header_full_text = header_full_text.replace(".", '')

        simplify_header_text = self.mini_header(header_full_text)

        if '!!!' in simplify_header_text and len(header_full_text.strip()):
            with open(f'header_mini_{self.time_start.strftime("%Y%m%d_%H%M%S")}.txt', mode='a') as fo:
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

    def parsing_content(self, card, doc_id):
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
            with open(f'content_error_{self.time_start.strftime("%Y%m%d_%H%M%S")}.txt', mode='a') as fo:
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

    def tlstory_get_date(self, tlstory):
        tlmonth, tlday, tlyear = tlstory.attrib.get('id').split('_')[1:]
        tlunits_date = [int('20' + str(tlyear)), int(tlmonth), int(tlday)]
        units_datetime = datetime.datetime(tlunits_date[0], tlunits_date[1], tlunits_date[2])
        return units_datetime.timestamp()
