import os
import pickle
import random
import string
from builtins import property
from time import sleep

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

from fbta_browser_constant import FBTABrowserConstant
from fbta_browser_title import FBTABrowserTitle
from fbta_configs import FBTAConfigs
from fbta_driver import FBTADriver
from fbta_main_browser import FBTAMainBrowser
from fbta_node_master import FBTANodeMaster
from fbta_settings import FBTASettings
from fbta_log import log


class FBTAWorkerBrowserS(FBTAMainBrowser):
    NONE = None

    def __init__(self, node_master: FBTANodeMaster):
        FBTAMainBrowser.__init__(self, FBTABrowserConstant.NODE_SLAVE, node_master.settings, node_master.configs)
        FBTABrowserTitle.__init__(self)
        self.__node_master = node_master

        self.__driver: FBTADriver = self._start_driver()

    def _check_internet_connect(self):
        return True

    def goto(self, url, stream=False):
        ret = self._get_secure(url, stream)
        if ret.encoding is not None:
            self._handle_status_to_process()
        self._handle_noscript(url)
        return ret

    def _get_secure(self, url, stream=False):
        load_time_out_retry = 0
        url_new = self._get_new_url(url)
        ret = 'NoContent'

        while True:
            if load_time_out_retry > 10:
                print(f':Browser: More retry use timeout')
                break
            try:
                return self._driver_get(url_new, stream)
            except TimeoutException as e:
                print(f':Browser: [{self.name}] Get method timeout retry={load_time_out_retry}')
                sleep(30)
                load_time_out_retry += 1
        return ret

    def start_browser(self):
        if self._settings.init_node_master_browser:
            self.__driver.add_cookie_from_node_master()
        else:
            self.__driver.add_cookie_from_file()

    def _start_driver(self) -> FBTADriver:
        driver = FBTADriver(self.__node_master)
        driver.implicitly_wait(self._const_timeout_loadpage)
        return driver

    def load_cookies(self):
        file_name = self._settings.dir_cookies + 'fbta_cookies.pkl'
        if os.path.exists(file_name):
            cookies = pickle.load(open(file_name, mode='rb'))
            for cookie in cookies:
                if 'expiry' in cookie:
                    del cookie['expiry']

                self.driver.add_cookie(cookie)

            self.driver.refresh()
            log(f':Browser: [{self.name}] Load Cookie OK')
        else:
            print(f':Browser: [{self.name}] Cannot find {file_name} file ')

    def _get_new_url(self, url):
        main_url = self.__node_master.url.getUrlFacebook()
        if main_url not in url:
            if 'http' not in url[:8]:
                url_new = self.__node_master.url.getUrlWithMain(url)
            else:
                url_new = url

        else:
            url_new = url
        return url_new

    def _driver_get(self, url, stream=False):
        tryagine_count = 0
        ret = 'browserNoContent'

        while True:
            if tryagine_count >= 50:
                print(f':wBrowser: {self.name} Very tried see you x_x')
                break
            try:
                return self.driver.get(url, stream=stream)
            except requests.ConnectionError:
                print(f':wBrowser: {self.name} Disconnect Tryagin={tryagine_count}')
                tryagine_count += 1
                sleep(30)

        return ret

    @property
    def driver(self) -> FBTADriver:
        return self.__driver
