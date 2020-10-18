import datetime
import random
import time

from fbta.fbta_global_database_manager import FBTADBManager
from fbta.fbta_node_master import FBTANodeMaster
from urllib.parse import parse_qs

from fbta.fbta_node_worker import FBTANodeWorker
from fbta.fbta_log import log


class FBTAHistoryDownloaderMethod:
    NONE = None
    """
    HistoryDownloadMethod Work like 'activity_download.py'
    but now it include in 'fbta_03_history_download_manager.py'
    """

    def __init__(self, node_master: FBTANodeMaster, worker_browser: FBTANodeWorker, db: FBTADBManager):
        self.__worker_driver = worker_browser.browser.driver
        self.db = db
        self.node_master = node_master
        self.__settings = self.node_master.settings
        self.__configs = self.node_master.configs

        self.__finishTime = self.__date2TimeStamp()

        self.slave_name = 0
        self.slave_class_name = 'u'

        self.page = {
            'current-url': '',
            'next-url': -1,
            'title': -1,
            'source': -1,
            'create': -1,
            'next-code': -1,
        }

    def addMonthUrl(self, url):
        self.page['current-url'] = url

    def checkIsShouldGoing(self):
        currentPointer = self.__getFacebookOldesrTime()
        pastPointer = self.__finishTime
        return currentPointer >= pastPointer

    def __getFacebookOldesrTime(self):
        return self.getTimeInActivity(self.__worker_driver.current_url).get('time-story-oldest', int(time.time()))

    def __date2TimeStamp(self) -> int:
        ret = int(
            datetime.datetime(
                self.__settings.date_process[0],
                self.__settings.date_process[1],
                self.__settings.date_process[2],
                tzinfo=datetime.timezone.utc).timestamp()
        )
        return ret

    def getNextUrl(self):
        return self.page['next-url']

    def __urlParsing(self, url):
        return parse_qs(str(url).split('/')[-1])

    def getTimeInActivity(self, url) -> dict:
        u: dict = self.__urlParsing(url)
        time0 = datetime.datetime.now()
        time0 = int(time0.replace(tzinfo=datetime.timezone.utc).timestamp())
        real = {
            'last-time': True,
            'old-time': True
        }
        timeend = int(u.get('allactivity?timeend', ['0'])[0])
        timestart = int(u.get('timestart', ['0'])[0])
        lastStoryTimestamp = int(u.get('lastStoryTimestamp', ['0'])[0])
        if lastStoryTimestamp == 0:
            lastStoryTimestamp = [str(int(time0 + 1))]
            real['last-time'] = False

        oldest = u.get('oldest', [str(int(time0 + 1))])[0]
        if len(oldest.split(':')) > 1:
            oldest = int(oldest.split(':')[0])
        else:
            oldest = int(oldest)
            real['old-time'] = False

        ret = {
            'time-end': timeend,
            'time-start': timestart,
            'time-story-last': lastStoryTimestamp,
            'time-story-oldest': oldest,
            'real': real
        }
        return ret

    def getPage_NextMoreLoad(self, showTitle=False, clustername='$'):
        # Find Next Link in this month
        load_next_title_el = self.__worker_driver.selector.xpath(
            '//div[contains(@id, "month_") and contains(@id, "_more_")]')
        if load_next_title_el:

            link = load_next_title_el.css('a::attr(href)').get()
            title = load_next_title_el.attrib['id']
            self.__setPageWithOnLoadData(link, title)

            if showTitle:
                log('\t\t$ [{name}] --> {title}'.format(name=self.slave_name, title=title))
            return True
        return False

    def __setPageWithOnLoadData(self, link, title):
        self.page = {
            'current-url': self.__worker_driver.current_url,
            'next-url': link,
            'title': title,
            'source': self.__worker_driver.page_source,
            'create': int(time.time()),
            'next-code': 1,
            'history-cluster-id': self.slave_name
        }

    def addPageToDb(self, doc_id):
        self.db.next_collection_insert_one(self.page)
        # addToDBProcessTime = time.time()
        # while True:
        #     try:
        #         self.db.next_collection_insert_one(self.page)
        #         break
        #     except:
        #         log('\t\t>$ [{name}] insert Error'.format(name=self.slave_name))
        #         if time.time() - addToDBProcessTime >= 60:
        #             log('\t\t>$ [{name}] insert Error AND GIVE UP'.format(name=self.slave_name))
        #             break
        #         time.sleep(random.random())

    def hasTimeline(self):
        return self.__checkTimeline()['code'] == 1

    def __checkTimeline(self):
        try:
            timeline = self.__worker_driver.selector.xpath('//div[contains(@id,"tlRecentStories_")]')
            return {'code': 1}
        except Exception as e:

            return {'code': 200}
