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
            url_new = self.__node_master.url.getUrlWithMain(url)
        else:
            url_new = url
        return url_new

    def _driver_get(self, url, stream=False):
        self.driver.get(url, stream=stream)

    @property
    def driver(self) -> FBTADriver:
        return self.__driver
