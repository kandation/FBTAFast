from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import time, datetime

from fbta_configs import FBTAConfigs
from fbta_settings import FBTASettings
from fbta_log import log
import threading
import logging


class FBTAActivityToCards:
    """
    export to MongoDB as card with format (all not None)
    'main-link' -> str,
    'header' -> dict
    'header' -> 'card-type' -> str,
    'header' -> 'header-links' -> list
    'header' -> 'header-links' -> [n] -> {text','uri'}
    'content' ->  dict,
    'content' -> 'content-html' -> str
    'content' -> 'content-text' -> str
    'content' -> privacy' -> str
    'raw' -> str
    'cid' -> int
    """

    def __init__(self, settings: FBTASettings, configs: FBTAConfigs):
        self.__settingsClass = settings
        self.__configsClass = configs

        self.dbName = self.__settingsClass.db_name
        self.client = MongoClient()
        self.db = self.client[self.dbName]

        self.dataCollection = self.db.get_collection(self.__configsClass.db_collection_01_page_name)

        self.cardCollection = self.db.get_collection(self.__configsClass.db_collection_02_card_name)

    def run(self):
        self.__analysis_dbFind()

    def __analysis_dbFind(self):
        startTImeAnalysis = time.time()
        log('Analysis start@', startTImeAnalysis)
        docs = self.dataCollection.find()

        self.__slave_parsing(docs)

        endTimeAnalysis = time.time()
        diffTimeAnalysis = endTimeAnalysis - startTImeAnalysis
        log('Analysis Stop@', endTimeAnalysis, 'Diff@', diffTimeAnalysis)

    def __slave_parsing(self, docs):
        """
        MongoDB --> Documents -> Pages
        Page is a Facebook Activity All
            Page
            |-<tlUnit_>
            ...|--<tlRecentStories_>
            ......|--<card><card><card>...<card>

        <card>
            <mainLink=[has/dont Has]
            <h3><a>Subject</a></h3>
            <content>
        """
        self.countCard = 0
        countDocs = 0
        startTime = time.time()
        log('Start Analysis Assign @', datetime.datetime.fromtimestamp(startTime))
        self.typeList = self.__getTypeList()

        for page in docs:
            soup = BeautifulSoup(page['source'], 'html.parser')

            tlunit = soup.findAll('div', id=re.compile('^tlUnit_'))

            log('TLUnit Len' + str(len(tlunit)))

            self.__slave_parsing_tlunit(page, tlunit)
            countDocs += 1

        endTime = time.time()
        diff = endTime - startTime
        log('Complted Analysis with', countDocs, 'End@', endTime, 'diff@', diff)

    def __slave_parsing_tlunit(self, page, tlunit):
        for units in tlunit:
            tlUnit_date_list = str(units.get('id')).replace('tlUnit_', '').split('_')
            (tlUnit_month, tlUnit_day, tlUnit_year) = tlUnit_date_list

            units_date = [int('20' + str(tlUnit_year)), int(tlUnit_month), int(tlUnit_day)]
            units_datetime = datetime.datetime(units_date[0], units_date[1], units_date[2])
            unit_timestamp = units_datetime.timestamp()

            unit = units.find('div', id=re.compile('^tlRecentStories_'))
            log('Unit len' + str(len(unit)))
            cards = unit.findAll('div', recursive=False)
            log('Card len' + str(len(cards)))
            cardPackData = self.__slave_parsing_tlunit_cards(page, cards)
            for cardData in cardPackData:
                cardData['cid'] = self.countCard
                cardData['date'] = units_date
                cardData['timestamp'] = unit_timestamp

                self.countCard += 1
                self.__insert2Db_card(cardData)

    def __insert2Db_card(self, cardData):
        try:
            log('Try insert card Id', self.countCard)
            self.cardCollection.insert_one(cardData)
        except Exception as e:
            log('Insert Card Error', e)
            exit()

    def __slave_parsing_tlunit_cards(self, page, cards):
        cardPack = []
        for card in cards:
            hasCard = card.find('div')
            if hasCard:
                mainLink = self.__card_processing_mainLink(card)
                if mainLink['next_action'] != '-1':
                    header = self.__card_processing_header(page, card)
                    content = self.__card_content(page, card)
                    cardData = {
                        'main-link': mainLink['main_link'],
                        'header': header,
                        'content': content,
                        'raw': str(hasCard),
                        'history-cluster-id': page['history-cluster-id']
                    }
                    cardPack.append(cardData)
        return cardPack

    def __card_content(self, page, card):
        p = card.findAll('h4')
        content = {'content-html': '', 'content-text': '', 'privacy': ''}
        if len(p) == 1:
            content['privacy'] = self.__linkCleanup(str(p[0].text).strip())
        if len(p) == 2:
            content['content-html'] = self.__linkCleanup(str(p[0].contents[0]).strip())
            content['content-text'] = self.__linkCleanup(str(p[0].text).strip())
            content['privacy'] = self.__linkCleanup(str(p[1].text).strip())
        return content

    def __card_processing_mainLink(self, card):
        a = card.find('a')
        action = {
            'main_link': '-1',
            'next_action': '-1'
        }

        if a:
            try:
                action = {
                    'main_link': a['href'],
                    'next_action': 'search-type'
                }
            except Exception as e:
                if str(e) == "'href'":
                    action = {
                        'main_link': '#',
                        'next_action': 'search-type-for-mainLink'
                    }
        return action

    def __linkCleanup(self, uri):
        return str(uri).replace('amp;', '')

    def __card_processing_header(self, page, card):
        headers = card.findAll('h3')

        for header in headers:
            if len(header.text) > 0:
                card_type = self.__card_type_condition(header)
                if card_type[1] != '0':
                    all_links = self.__card_processing_header_findLinkAll(card_type, header)
                    headerPage = {
                        'card-type': str(card_type[0]).lower(),
                        'header-links': all_links,
                        'header-raw': str(header),
                        'header-text': header.text
                    }
                    return headerPage

    def __getTypeList(self):
        """
                 1 = Owener(subject)
                 2 = verb/Action
                 3 = Another(subject)
                 4 = Object
                 5 = source(object)
                 sp = spacial case (One tag can be more types)
                 dx = dont interest
                 ev = event (not parsing but interrest)

                """
        dd = {
            '124': ['shared', 'posted in', 'via', 'reviewed', 'subscribed', 'was at', 'uploaded', 'going to'],
            '1234': ['likes', 'commented', 'replied', 'reacted', 'liked', 'was tagged', 'voted'],
            '12435': ['saved'],
            '1': ['updated', 'was live', 'approved', 'published', 'using', 'edited', 'changed'],
            '123': ['replied', 'wrote on', 'followed', 'mentioned', 'became', 'is with', 'was with', 'is at', 'sent',
                    'poked'],
            'sp': ['added', 'feeling', 'created'],
            'dx': ['played', 'breeding', 'evolved', 'took', 'earned', 'new high score', 'celebrating', 'solved'],
            'ev': ['interested', 'watching', 'was playing']
        }
        tn = []
        for k, val in dd.items():
            for v in val:
                tn.append((v, k))
        return tn

    def __card_type_condition(self, header):
        for tp in self.typeList:
            if tp[0] in header.text:
                return tp
        return ('0', '0')

    def __card_processing_header_findLinkAll(self, card_type, header):
        '''{sub}{cmd}{owner}{object}'''
        headerClassify = {}
        alinks_in_header = header.findAll('a')
        header_link_all = self.__card_header_classify_link(alinks_in_header)
        return header_link_all

    def __card_type_check_realType(self, oldType, links):
        thinking_type = {
            'likes': ['13']
        }

    def __card_processing_header_typeLengthCheck(self, card_type, links):
        return len(card_type) == len(links)

    def __card_processing_header_type_translate(self, type_number):
        typeList = {
            '1': ('owner', True),
            '2': ('action', False),
            '3': ('another', True),
            '4': ('object', True),
            '5': ('source', True)
        }
        return typeList[str(type_number)]

    def __card_header_classify_link(self, links):
        ret = []
        for link in links:
            p = {}
            p['text'] = link.text
            try:
                p['uri'] = link['href']
            except:
                p['uri'] = '#'
            ret.append(p)
        return ret
