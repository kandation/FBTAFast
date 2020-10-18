from typing import List, Optional

from parsel import Selector

from fbta.fbta_browser_worker_new import FBTAWorkerBrowserS
from fbta.fbta_node_master import FBTANodeMaster
from pprint import pprint
import datetime
from json import dumps, loads

from fbta.fbta_log import log


class FBTAYearBox:
    """
        YearBox is timeline load its work with activity log
    """

    def __init__(self, master_node: FBTANodeMaster):
        self.node_master = master_node
        self.browser = FBTAWorkerBrowserS(master_node)
        self.browser.start_browser()
        self.year_box = None

    def run(self):
        self.__goto()
        self.year_box = self.__findMonthEachYear()

    def getYearbox(self) -> dict:
        if self.year_box is None:
            self.run()
        return self.year_box

    def __findMonthEachYear(self):
        nowMonth_SLN = self.__getPreloadMonth()
        print(nowMonth_SLN)
        nowYearMonth = self.__scanMonth(nowMonth_SLN)

        year_box = self.__findYearBox()

        print('findMonthEachYear')

        for year_num in year_box:
            each_month_url = self.node_master.url.getUrlFacebook() + year_box[year_num]['url']
            self.browser.goto(each_month_url)
            data_all_month = self.__getPreloadMonth()
            year_box[year_num]['month'] = self.__scanMonth(data_all_month)

        year_box['current'] = {
            'url': -1,
            'year': str(datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).strftime('%Y')),
            'month': nowYearMonth
        }

        return year_box

    def __goto(self):
        self.browser.goto(self.node_master.url.getUrlActivityLog())

    def __getPreloadMonth(self, month='None'):
        if month == 'None':
            preload_month = self.browser.driver.selector.xpath(
                '//div[contains(@id, "month_") and not(contains(@id, "_more_"))]')
        else:
            preload_month = self.browser.driver.selector.xpath(
                '//div[contains(@id, "month_' + month + '_") and not(contains(@id, "_more_"))]')

        print(self.browser.driver.title, self.browser.driver.current_url)

        return preload_month

    def __getPreloadYear(self) -> List[Optional[Selector]]:
        preload_year = self.browser.driver.selector.xpath(
            '//div[contains(@id, "year_") and not(contains(@id, "_more_"))]')
        return preload_year

    def __findYearBox(self):
        log_r = {}
        data_all_year = self.__getPreloadYear()
        for i in data_all_year:
            temp_ = {
                'url': 0,
                'year': 0,
                'month': []
            }

            year_link_element = i.css('a')
            year_link = year_link_element.attrib['href']

            header_year = self.__reg_paser(year_link)

            if header_year not in log_r:
                temp_['url'] = year_link
                temp_['year'] = year_link_element.xpath('text()').get()
                log_r[str(header_year)] = temp_

        return log_r

    def __parserMonth(self, month_num: Selector):
        month_element = month_num.css('a')

        month_link = month_element.xpath('@href').get()

        header_month = self.__reg_paser(month_link)
        text_month = month_element.xpath('text()').get()

        return {'header_month': header_month, 'text_month': text_month, 'month_link': month_link}

    def __reg_paser(self, month: str):
        import urllib.parse as urlparse
        parsed = urlparse.urlparse(month)
        return urlparse.parse_qs(parsed.query).get('section_id')[0]

    def __scanMonth(self, data_all_month):
        year_box = []
        for month_num in data_all_month:
            paser_month = self.__parserMonth(month_num)

            if len(paser_month['text_month']) > 4:
                stampTimeStr = str(paser_month['header_month']).split('_')
                stampTime = datetime.datetime(int(stampTimeStr[1]), int(stampTimeStr[2]), 1).replace(
                    tzinfo=datetime.timezone.utc).timestamp()

                temp_month_dict = {
                    'url': paser_month['month_link'],
                    'title': paser_month['header_month'],
                    'text': paser_month['text_month'],
                    'date': stampTime
                }

                year_box.append(temp_month_dict)

        return year_box
