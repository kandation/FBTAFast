import os
import pickle

import requests
from bs4 import BeautifulSoup
from parsel import Selector

from fbta_log import log
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
        self.__raw_url = 'init'

        self.__header = self.session.headers

    def start_session(self):
        self.add_cookie_from_node_master()

    @property
    def session(self) -> requests.Session():
        return self._session

    def get_headers(self):
        return self.__header

    def set_header_chrome(self):
        self.__header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
        self.session.headers.update(self.__header)

    def set_header_firefox(self):
        self.__header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
        self.session.headers.update(self.__header)

    def set_headers_custome(self, headers):
        self.session.headers.update(headers)

    def get(self, url, stream=False, show_url=True) -> requests.Response:
        self.__raw_url = url
        if show_url:
            log(f'>> :Driver: stream={stream} get {url} ')
        self._respond = self._session.get(url, headers=self.__header, stream=stream, allow_redirects=True)
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
    def raw_url(self):
        return self.__raw_url

    @property
    def current_url(self):
        if self._respond:
            return self._respond.url
        return ''

    @property
    def page_source(self):
        return str(self._respond.content.decode(encoding=self._respond.encoding, errors='ignore'))

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
        file_name = self.__settings.dir_cookies + 'fbta_cookies_old.pkl'
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
        self.session.cookies.set(name, None)

    def set_page_load_timeout(self, timeout):
        self.implicitly_wait(timeout)
