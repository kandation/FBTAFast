import os
import pickle

import requests
from bs4 import BeautifulSoup
from parsel import Selector

from fbta_node_master import FBTANodeMaster


class FBTADriver:
    # TODO 620818 New project with fast browser
    # TODO 620818 Try https://tryolabs.com/blog/2017/11/22/requestium-integration-layer-requests-selenium-web-automation/
    # TODO 620818 Temporary Achive: because we will write new all
    def __init__(self, node_master: FBTANodeMaster):
        self._session = requests.Session()
        self._respond: requests.Response = None
        self.__node_master = node_master
        self.__settings = node_master.settings
        self.__configs = node_master.configs
        self.__soup: BeautifulSoup = None
        self.__selector: Selector = None
        self.__request_Timeout = None

    def start_session(self):
        self.add_cookie_from_node_master()

    @property
    def session(self) -> requests.Session():
        return self._session

    def get(self, url, stream=False) -> requests.Response:
        print(f'>> :Driver: stream={stream} get {url} ')
        self._respond = self._session.get(url, stream=stream, allow_redirects=True)
        if self._respond.encoding is not None:
            self.__soup = BeautifulSoup(self._respond.content, 'lxml')
            self.__selector = Selector(self._respond.text)
        else:
            self.__soup = None
            self.__selector = None

        return self._respond

    def get_stream(self, url):
        self._respond = self._session.get(url, allow_redirects=True)

    @property
    def current_url(self):
        if self._respond:
            return self._respond.url
        return ''

    @property
    def page_source(self):
        return str(self._respond.content, encoding=self._respond.encoding)

    def get_title(self):
        # return self.__soup.find('title').text
        return self.selector.css('title::text').get()

    @property
    def title(self):
        return self.get_title()

    def refresh(self):
        self.get(self.current_url)

    def add_cookie_from_node_master(self):
        if self.__settings.use_nodeMaster:
            request_cookies_browser = self.__node_master.browser.driver.get_cookies()
            for c in request_cookies_browser:
                self._session.cookies.set(c['name'], c['value'])
        else:
            print(':FastDriver: Cannot Load Cookie Frome master becuse has not NodeMaster')

    def add_cookie(self, cookie):
        for key in cookie:
            self._session.cookies.set(str(key), str(cookie[key]))

    def get_cookies(self):
        ret = []
        for cookie in self._session.cookies:
            ret.append({'name': cookie.name,
                        'path': cookie.path,
                        'value': cookie.value
                        })
        return ret

    def quit(self):
        self._session.close()

    def delete_all_cookies(self):
        self._session.cookies.clear()

    @property
    def selector(self) -> Selector:
        return self.__selector

    @property
    def bs(self) -> BeautifulSoup:
        return self.__soup

    def find_element_by_name(self, name):
        return self.__selector.css(f'[name="{str(name)}"]').get()
        # return self.__soup.select_one(f'[name="{str(name)}"]')

    def add_cookie_from_file(self):
        self.__load_cookies()

    def find_element_by_xpath(self, xpath):
        return self.__selector.xpath(xpath).get(0)

    def find_elements_by_xpath(self, xpath):
        return self.__selector.xpath(xpath)

    def __load_cookies(self):
        file_name = self.__settings.dir_cookies + 'fbta_cookies.pkl'
        if os.path.exists(file_name):
            cookies = pickle.load(open(file_name, mode='rb'))
            for cookie in cookies:
                self._session.cookies.set(cookie['name'], cookie['value'])

    def implicitly_wait(self, timeout):
        self.__request_Timeout = timeout

    def get_cookie(self, name):
        for cookie in self._session.cookies:
            if name == cookie.name:
                return {'name': cookie.name, 'value': cookie.value}
        return False

    def delete_cookie(self, name):
        pass

    def set_page_load_timeout(self, timeout):
        self.implicitly_wait(timeout)
