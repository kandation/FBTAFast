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
from fbta_settings import FBTASettings
from fbta_log import log


class FBTANewBrowser(FBTABrowserTitle):
    NONE = None

    def __init__(self, duty: FBTABrowserConstant, settings: FBTASettings, configs: FBTAConfigs):
        self.duty = duty
        FBTABrowserTitle.__init__(self)
        self.__configs = configs
        self.__settings = settings

        self.__const_timeout_loadpage = 120
        self.name = self.__randomString(5)

        self.__test_end_killer = self.__settings.kill_driver_on_end

        self.__chrome_options = Options()
        # IF RUN IN MODE NO-JS CHROME USE 2
        # self.__chrome_options.add_experimental_option("prefs",
        #                                               {'profile.managed_default_content_settings.javascript': 0})
        print(self.__configs.window_size_width, self.__configs.window_size_height)

        self.__chrome_options.add_argument(
            '--window-size={w},{h}'.format(w=self.__configs.window_size_width,
                                           h=self.__configs.window_size_height))
        self.__driver = None

        self.__use_noscript = True

        self.__fb_scope = FBTABrowserConstant.FBSCOPE_GLOBAL

        self.__signal = FBTABrowserConstant.SIGNAL_NORMAL_START

    def start_browser(self):
        self.__driver = self.__start_master_driver()

    @property
    def driver(self) -> webdriver.Chrome:
        return self.__driver

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name=None):
        if name:
            self.__name = name
            self.__alway_check_masterduty_change_name()

    @property
    def fb_scope(self):
        return self.__fb_scope_hidden

    @fb_scope.setter
    def fb_scope(self, scope: FBTABrowserConstant):
        self.__fb_scope_hidden = scope

    def has_driver(self):
        return self.driver is not None

    def __randomString(self, stringLength=6) -> str:
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    def use_no_script(self, use=True):
        self.__use_noscript = use

    def __start_master_driver(self) -> webdriver.Chrome:
        if self.__settings.use_nodeMaster:
            driver = webdriver.Chrome(self.__settings.driver_path,
                                      chrome_options=self.__chrome_options)
            driver.implicitly_wait(self.__const_timeout_loadpage)
        else:
            driver = None
        return driver

    def __check_internet_connect(self):
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
                sleep(self.__configs.time_retry_connectError)
            except Exception as e:
                log(f':Browser: [{self.name}] Internet Check Error = {e}')
                sleep(5)

            if retry == 100:
                log(f':Browser: [{self.name}] Internet NotConnect Giveup with retry {retry}')
                break
        return False

    def __has_browser_noscript(self):
        is_noscript = True if self.driver.get_cookie('noscript') is not None else False
        return is_noscript

    def __handle_noscript(self, url):
        if self.__use_noscript:
            self.__handle_noscript_use_noscript(url)
        else:
            if self.__has_browser_noscript():
                self.driver.delete_cookie('noscript')
                self.driver.refresh()

    def __handle_noscript_use_noscript(self, url):
        if not self.__has_browser_noscript():
            retry_addcookie = 50
            while retry_addcookie > 0:
                try:
                    self.driver.add_cookie({'name': 'noscript', 'value': '1'})
                    break
                except:
                    sleep(self.__configs.time_retry_addCookie)
                    if not self.__check_internet_connect():
                        retry_addcookie -= 1
                    else:
                        self.__get_secure(url)

            self.driver.refresh()

    @property
    def duty(self):
        return self.__duty

    @duty.setter
    def duty(self, d: FBTABrowserConstant):
        self.__duty = d

    @property
    def title(self) -> str:
        return self.driver.title

    def save_cookies(self):
        file_name = self.__settings.dir_cookies + 'fbta_cookies.pkl'
        pickle.dump(self.driver.get_cookies(), open(file_name, mode='wb'))
        log(f':Browser: [{self.name}] Save Cookie OK')

    def load_cookies(self):
        file_name = self.__settings.dir_cookies + 'fbta_cookies.pkl'
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

    def __alway_check_masterduty_change_name(self):
        if self.__is_master:
            self.__name = 'Master'
        else:
            if str(self.name).lower() == 'master':
                print(f':Browser: Random New Name [{self.name}]')
                self.name = self.__randomString()

    @property
    def browser_is_master(self) -> bool:
        self.__alway_check_masterduty_change_name()
        return self.__is_master

    @property
    def login_signal(self):
        self.__check_login()
        return self.__signal

    def __check_login(self):
        self.__fb_scope, _ = self.check_login_type(self.__fb_scope)
        title_status = self.check_title_status(self.__fb_scope)
        self.__signal = title_status[1]
        # print('\t\t\t\t',self.__signal)

    def goto(self, url):
        self.__check_internet_connect()
        self.__get_secure(url)
        self.__check_login()
        self.__handle_noscript(url)

    def __get_secure(self, url):
        load_time_out_retry = 0
        while True:
            if load_time_out_retry > 10:
                print(f':Browser: More retry use timeout')
                break
            try:
                self.driver.get(url)
                self.driver.set_page_load_timeout(30)
                break
            except  TimeoutException as e:
                print(f':Browser: [{self.name}] Get method timeout retry={load_time_out_retry}')
                sleep(30)
                load_time_out_retry += 1

    def killdriver(self):
        try:
            self.driver.quit()
            log(f':Browser: [{self.name}] Driver Killed (✖╭╮✖)')
        except Exception as e:
            log(f':Browser: [{self.name}] Driver Kill Error as {e}')

    @property
    def __is_master(self):
        return self.duty == FBTABrowserConstant.NODE_MASTER

    def __del__(self):
        if self.__test_end_killer:
            self.killdriver()
