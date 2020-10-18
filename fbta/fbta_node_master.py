import time
import types

from fbta.fbta_browser_selenium import FBTABrowserSelenium
from fbta.fbta_browser_constant import FBTABrowserConstant
from fbta.fbta_configs import FBTAConfigs
from fbta.fbta_settings import FBTASettings

from fbta.fbta_url import FBTAUrl


class FBTANodeMaster:
    NONE = None

    def __init__(self, settings: FBTASettings, configs: FBTAConfigs):
        self.__settings = settings
        self.__configs = configs

        self.__browser: FBTABrowserSelenium = FBTABrowserSelenium(
            FBTABrowserConstant.NODE_MASTER,
            self.settings,
            self.configs)

        self.__browser.start_browser()

        self.__driver = self.__browser.driver

        self.__url: FBTAUrl = FBTAUrl(self.settings, self.configs)

        self.__time_cooldown_login = 0

        self.__status = {
            'locked': False
        }

        self.__time_lock_cooldown = 0

    @property
    def configs(self):
        return self.__configs

    @property
    def settings(self):
        return self.__settings

    @property
    def browser(self) -> FBTABrowserSelenium:
        return self.__browser

    @property
    def url(self) -> FBTAUrl:
        return self.__url

    def set_locked(self):
        self.__status['locked'] = True

    def set_unlocked(self):
        self.__status['locked'] = False

    def is_locked(self):
        return self.__status.get('locked', False)

    def is_locked_cooldown_timeout(self):
        return (time.time() - self.__time_lock_cooldown) >= self.configs.time_master_lock_cooldown

    def __update_username(self):
        if '@' in self.__settings.username:
            self.__settings.set_user_information('username-type', 'email')
        elif '+' == str(self.__settings.username)[0]:
            self.__settings.set_user_information('username-type', 'phone')
        else:
            self.__update_username_user_or_phone()

    def __update_username_user_or_phone(self):
        try:
            num = str(int(self.__settings.username))
            user_length = len(self.__settings.username)

            if 10 <= user_length <= 11:
                self.__settings.set_user_information('username-type', 'phone/profile-id')
            else:
                self.__settings.set_user_information('username-type', 'profile-id')
        except:
            self.__settings.set_user_information('username-type', 'normal')

    def __getPassword(self):
        from fbta_encrypt import FBTAEncrypt
        pwd = FBTAEncrypt()
        pwd.loadKey(self.__settings.password_key)
        pwd.loadPassword(self.__settings.password_enc)
        pwd = pwd.decrypt()
        return pwd

    def start(self):
        if self.settings.init_node_master_browser:
            self.__login_cookies_switching()

    def login_without_cookie(self):
        self.__driver.delete_all_cookies()
        self.goto_login()
        if self.settings.use_nodeMaster_loadCookie:
            self.browser.save_cookies()

    def goto_login(self):
        if self.__browser.browser_is_master:
            self.__browser.goto(self.url.getUrlFacebook())
            self.__login_method()

    def __login_method(self):
        try:
            email = self.__driver.find_element_by_name('email')
            email.send_keys(self.settings.username)
            print("Master Email Id entered...")
            password = self.__driver.find_element_by_name('pass')
            password.send_keys(self.__getPassword())
            print("Master Password entered...")
            loginbutton = self.__driver.find_element_by_name('login')
            loginbutton.click()
        except Exception as e:
            self.__status['login'] = False
            print('Master Login Error')
            # exit()
            raise e

        self.__status['login'] = True
        self.__status['lock-master'] = False

        userInfo = self.__after_login_update_profile()

        self.settings.set_user_information('profile', userInfo)
        self.__browser.goto(self.url.getUrlActivityLog())
        self.cooldownLoginTime = time.time()

    def __after_login_update_profile(self):
        self.__browser.goto(self.url.getUrlProfile())

        curl = self.__driver.current_url
        tim = self.__driver.find_element_by_xpath('//div[@id="m-timeline-cover-section"]')

        realName = tim.find_element_by_css_selector('strong')
        realNameString = str(realName.text)

        import re
        p = re.compile(r'<.*?>')
        realNameString = p.sub('', realNameString)

        try:
            altenate = realName.find_element_by_css_selector('span')
            realNameString = realNameString.replace(altenate.text, '')
        except:
            pass

        alinks = tim.find_elements_by_tag_name('a')
        userId = None
        for a in alinks:
            if 'Activity Log' in a.text:
                uid = str(a.get_attribute('href')).replace(self.url.getUrlFacebook(), '').split('/')
                uid = list(filter(None, uid))
                print(uid)
                userId = uid[0]

        realUsername = str(curl).replace(self.url.getUrlFacebook(), '').replace('?_rdr#_', '')

        userData = {
            'username': realUsername,
            'name': str(realNameString).strip(),
            'uid': userId
        }

        return userData

    def set_signal_login_not_sucess(self):
        self.__status['login'] = False

    def is_login_sucess(self):
        return self.__status.get('login', False)

    def goto(self, url):
        self.__browser.goto(url)

    def is_should_login(self):
        self.__driver.refresh()
        return self.__browser.login_signal

    def __login_cookies_switching(self):
        self.goto(self.url.getUrlFacebook())
        is_new_login = False
        if self.settings.use_nodeMaster_loadCookie:
            try:
                self.login_with_cookie()
            except Exception as e:
                print('/n', '=' * 30)
                print(':NodeMaster: Cannot Run cookie')
                print('=' * 30)
                print(e)
                print('=' * 30)
                exit()
                is_new_login = True
        else:
            print(':NodeMaster: New Login by command')
            is_new_login = True

        if is_new_login:
            print(':NodeMaster: ==== Do Login ====')
            self.goto_login()
            self.__browser.save_cookies()

    def login_with_cookie(self):
        print(':NodeMaster: ------ Use cookies --------')
        self.__browser.load_cookies()
        is_should_login = self.is_should_login()
        if is_should_login:
            print(':NodeMaster: |Error|: MasterNode Cannot use Old cookies Try Renew Login')
            self.login_without_cookie()
        self.__status['login'] = not is_should_login

    def slave_waiting_node_master(self, slave_name: str):
        if self.settings.init_node_master_browser:
            while not self.is_login_sucess():
                print(f':Master: Slave [{slave_name}] waiting NODE_MASTER')
                time.sleep(2)
            time.sleep(5)

    def slave_call_master_new_login(self, slave_cls, url):
        if not self.is_locked() and self.is_locked_cooldown_timeout():
            self.set_locked()

            print(f':Master: Slave [{slave_cls.name}] know LOGIN_OUT')
            is_should_login = self.is_should_login()
            if is_should_login:
                self.set_signal_login_not_sucess()
                self.login_without_cookie()
                self.slave_waiting_node_master(slave_cls.name)
                self.browser.save_cookies()
            else:
                slave_cls.auto_load_cookies()
                self.slave_waiting_node_master(slave_cls.name)
                time.sleep(2)
                slave_cls.browser.goto(url)

            self.set_unlocked()
        else:
            self.slave_waiting_node_master(slave_cls.name)
            print(f':Master:\tslave [{slave_cls.name}] OK and LoadCookies')
            slave_cls.browser.driver.delete_all_cookies()
            while True:
                try:
                    slave_cls.auto_load_cookies()
                    break
                except:
                    print(f':Master:\t\t > Slave [{slave_cls.name}] Cannot get Cookies try agin')
                time.sleep(2)

        slave_cls.browser.goto(url)
