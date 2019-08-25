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
from fbta_main_browser import FBTAMainBrowser
from fbta_settings import FBTASettings
from fbta_log import log


class FBTABrowserSelenium(FBTAMainBrowser):
    NONE = None

    def __init__(self, duty: FBTABrowserConstant, settings: FBTASettings, configs: FBTAConfigs):
        FBTAMainBrowser.__init__(self, duty, settings, configs)
        FBTABrowserTitle.__init__(self)


        self.__chrome_options = Options()
        print(self._configs.window_size_width, self._configs.window_size_height)
        self.__chrome_options.add_argument(
            '--window-size={w},{h}'.format(w=self._configs.window_size_width,
                                           h=self._configs.window_size_height))

        self.__driver = None



    @property
    def driver(self) -> webdriver.Chrome:
        return self.__driver

    def start_browser(self):
        self.__driver = self._start_driver()

    def _start_driver(self) -> webdriver.Chrome:
        if self._settings.init_node_master_browser:
            driver = webdriver.Chrome(self._settings.driver_path,
                                      chrome_options=self.__chrome_options)
            driver.implicitly_wait(self._const_timeout_loadpage)
        else:
            driver = None
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
        return url

    def _driver_get(self, url, stream=False):
        self.driver.get(url)
