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
from abc import ABCMeta, abstractmethod


class FBTAMainBrowser(FBTABrowserTitle, metaclass=ABCMeta):
    NONE = None

    def __init__(self, duty: FBTABrowserConstant, settings: FBTASettings, configs: FBTAConfigs):
        self.duty = duty
        FBTABrowserTitle.__init__(self)
        self._configs = configs
        self._settings = settings

        self._const_timeout_loadpage = 120
        self.name = self.__randomString(5)

        self.__test_end_killer = self._settings.kill_driver_on_end

        self.__use_noscript = True

        self.__fb_scope = FBTABrowserConstant.FBSCOPE_GLOBAL

        self.__signal_login: bool = True
        self.__signal_need_restart_browser: bool = False
        self.__signal_reload_content: bool = False
        self.__signal_reload_content_once: bool = False

        self.__title_status = FBTABrowserConstant.STATUS_NORMAL

    @abstractmethod
    def start_browser(self):
        pass

    def has_driver(self):
        return self.driver is not None

    def __randomString(self, stringLength=6) -> str:
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    def use_no_script(self, use=True):
        self.__use_noscript = use

    @abstractmethod
    def _start_driver(self) -> webdriver.Chrome:
        pass

    @abstractmethod
    def _check_internet_connect(self):
        pass
    def __has_browser_noscript(self):
        is_noscript = True if self.driver.get_cookie('noscript') is not None else False
        return is_noscript

    def _handle_noscript(self, url):
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
                    print('browser ADDDDDDDDDDDDDDDDDD NOSCRIPT')
                    self.driver.add_cookie({'name': 'noscript', 'value': '1'})
                    break
                except:
                    sleep(self._configs.time_retry_addCookie)
                    if not self._check_internet_connect():
                        retry_addcookie -= 1
                    else:
                        self.__get_secure(url)

            self.driver.refresh()

    def save_cookies(self):
        file_name = self._settings.dir_cookies + 'fbta_cookies_old.pkl'
        pickle.dump(self.driver.get_cookies(), open(file_name, mode='wb'))
        log(f':Browser: [{self.name}] Save Cookie OK')

    @abstractmethod
    def load_cookies(self):
        pass

    def __always_check_master_duty_change_name(self):
        if self.__is_master:
            self.__name = 'Master'
        else:
            if str(self.name).lower() == 'master':
                print(f':Browser: Random New Name [{self.name}]')
                self.name = self.__randomString()

    def __update_status(self):
        self.__title_status = self.detect_content_status(self.__fb_scope)

    def __update_fb_scope(self):
        self.__fb_scope, _ = self.check_login_type(self.__fb_scope)

    def _handle_status_to_process(self):
        self.__update_status()
        self.__update_fb_scope()
        if self.__title_status == FBTABrowserConstant.STATUS_NORMAL:
            self.__update_signal()

        elif self.__title_status == FBTABrowserConstant.STATUS_LOGIN_AGAIN:
            self.__update_signal(login=True)

        elif self.__title_status == FBTABrowserConstant.STATUS_CONTENT_RELOAD:
            self.__update_signal(reload=True)

        elif self.__title_status == FBTABrowserConstant.STATUS_CONTENT_RELOAD_ONCE:
            self.__update_signal_once(content_once=True)

    def __update_signal(self, login=False, restart=False, reload=False):
        self.__signal_login = login
        self.__signal_need_restart_browser = restart
        self.__signal_reload_content = reload

    def __update_signal_once(self, content_once=False):
        self.__signal_reload_content_once = content_once

    def goto(self, url, stream=False):
        self._check_internet_connect()
        self.__get_secure(url, stream)
        self._handle_status_to_process()
        self._handle_noscript(url)

    def __get_secure(self, url, stream=False):
        load_time_out_retry = 0
        url_new = self._get_new_url(url)

        while True:
            if load_time_out_retry > 10:
                print(f':Browser: More retry use timeout')
                break
            try:
                self._driver_get(url_new, stream)
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
            log(f':Browser: [{str(self.name)}] Driver Kill Error as {e}')

    def __del__(self):
        if self.__test_end_killer:
            self.killdriver()

    @abstractmethod
    def _get_new_url(self, url):
        pass

    @abstractmethod
    def _driver_get(self, url, stream=False):
        pass

    @property
    @abstractmethod
    def driver(self):
        raise Exception(':mainBrowser:Plase init driver propertie')

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name=None):
        if name:
            self.__name = name
            self.__always_check_master_duty_change_name()

    @property
    def fb_scope(self):
        return self.__fb_scope_hidden

    @fb_scope.setter
    def fb_scope(self, scope: FBTABrowserConstant):
        self.__fb_scope_hidden = scope

    @property
    def __is_master(self) -> bool:
        return self.duty == FBTABrowserConstant.NODE_MASTER

    @property
    def browser_is_master(self) -> bool:
        self.__always_check_master_duty_change_name()
        return self.__is_master

    @property
    def has_signal_loop(self)->bool:
        return any([self.__signal_login,self.__signal_reload_content, self.__signal_need_restart_browser])

    @property
    def has_signal_once(self) -> bool:
        return any([self.__signal_reload_content_once])

    @property
    def login_signal(self) -> bool:
        self._handle_status_to_process()
        return self.__signal_login

    @property
    def duty(self) -> FBTABrowserConstant:
        return self.__duty

    @duty.setter
    def duty(self, d: FBTABrowserConstant):
        self.__duty = d

    @property
    def title(self) -> str:
        return self.driver.title

    @property
    def signal_restart_browser(self) -> bool:
        return self.__signal_need_restart_browser

    @property
    def signal_reload_content(self) -> bool:
        return self.__signal_reload_content

    @property
    def signal_reload_content_once(self) -> bool:
        return self.signal_reload_content_once

    def reset_loop_signal(self):
        self.__update_signal()
