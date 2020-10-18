import os
import pickle
import random
import string
from builtins import property
from time import sleep

import requests
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

from fbta.fbta_browser_constant import FBTABrowserConstant
from fbta.fbta_browser_title import FBTABrowserTitle
from fbta.fbta_configs import FBTAConfigs
from fbta.fbta_main_browser import FBTAMainBrowser
from fbta.fbta_settings import FBTASettings
from fbta.fbta_log import log


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

        self.__setting = settings
        if settings.headerless:
            self.__chrome_options.add_argument("--headless")

        self.__driver = None

    def _check_internet_connect(self):
        url = 'https://gist.githubusercontent.com/kandation/df77802e4ba542a20d2d92bfeea45a5d/raw/00fb580a14ec12087acf8e3ab2276f5b9a25115d/private_internet_connect_check.txt'
        timeout = 10
        retry = 0
        while True:
            try:
                k = requests.get(url, timeout=timeout)
                if k.text == 'GGEZNOOBINTERNETCONNECT':
                    return True
            except requests.ConnectionError:
                log(f':Browser: [{self.name}] Internet Not Connected@retry={retry}')
                retry += 1
                sleep(self._configs.time_retry_connectError)
            except Exception as e:
                log(f':Browser: [{self.name}] Internet Check Error = {e}')
                sleep(5)

            if retry == 100:
                log(f':Browser: [{self.name}] Internet NotConnect Giveup with retry {retry}')
                break
        return False

    @property
    def driver(self) -> webdriver.Chrome:
        return self.__driver

    def start_browser(self):
        self.__driver = self._start_driver()

    def _start_driver(self) -> webdriver.Chrome:
        if self._settings.init_node_master_browser:
            try:
                driver = webdriver.Chrome(self._settings.driver_path,
                                          chrome_options=self.__chrome_options)
            except selenium.common.exceptions.SessionNotCreatedException as e:
                print('ChromeDriver not support chrome version please Download '
                      'https://chromedriver.chromium.org/downloads\n'
                      'And Edit ChromeDriver path in your settings')
                # raise e
                exit()
            except BaseException as base_exp:
                raise base_exp
            driver.implicitly_wait(self._const_timeout_loadpage)
        else:
            driver = None
        return driver

    def load_cookies(self):
        file_name = self._settings.dir_cookies + 'fbta_cookies_old.pkl'
        file_name_json = self._settings.dir_cookies + 'fbta_cookies.json'
        if self.__setting.json_cookie:
            if os.path.exists(file_name_json):
                import json
                cookies = json.loads(open(file_name_json, mode='r', encoding='utf8').read())
                for cookie in cookies:
                    if cookie['name'] != 'sameSite':
                        self.driver.add_cookie(cookie)
            else:
                print(f':Browser: [{self.name}] Cannot find {file_name} file ')
        else:
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

    def __del__(self):
        if self.driver:
            self.driver.close()
