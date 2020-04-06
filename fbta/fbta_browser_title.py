import datetime

from selenium import webdriver

from fbta_browser_constant import FBTABrowserConstant
from abc import ABCMeta, abstractmethod

from fbta_log import log


class FBTABrowserTitle(metaclass=ABCMeta):

    def __init__(self):
        self.__checker_login_url: dict = {
            'login/': FBTABrowserConstant.FBSCOPE_GLOBAL,
            'login.php?': FBTABrowserConstant.FBSCOPE_GLOBAL,
            'story.php?story_fbid=': FBTABrowserConstant.FBSCOPE_PRIVATE
        }

        self.__checker_login_tile = {
            'เข้าสู่ระบบหรือสมัครใช้งาน': {
                'do': FBTABrowserConstant.STATUS_LOGIN_AGAIN,
                'step': [
                    FBTABrowserConstant.DOING_TITLE_CHECK_ONLY
                ]
            },
            'เข้าสู่ระบบ facebook': {
                'do': FBTABrowserConstant.STATUS_LOGIN_AGAIN,
                'step': [
                    FBTABrowserConstant.DOING_TITLE_CHECK_ONLY
                ]
            },
            'Facebook - เข้าสู่ระบบหรือสมัครใช้งาน': {
                'do': FBTABrowserConstant.STATUS_LOGIN_AGAIN,
                'step': [
                    FBTABrowserConstant.DOING_TITLE_CHECK_ONLY
                ]
            },
            'Log in to Facebook': {
                'do': FBTABrowserConstant.STATUS_LOGIN_AGAIN,
                'step': [
                    FBTABrowserConstant.DOING_TITLE_CHECK_ONLY
                ]
            },
            'การตรวจสอบสถานะความปลอดภัย': {
                'do': FBTABrowserConstant.STATUS_BROWSER_RESTART,
                'step': [
                    FBTABrowserConstant.DOING_TITLE_CHECK_ONLY
                ]
            },
            'mobile_login_bar': {
                'do': FBTABrowserConstant.STATUS_LOGIN_AGAIN,
                'step': [
                    FBTABrowserConstant.DOING_CONTENT_CHECK_ONLY
                ]
            },
            'เข้าร่วม Facebook หรือเข้าสู่ระบบเพื่อดำเนินการต่อ': {
                'do': FBTABrowserConstant.STATUS_LOGIN_AGAIN,
                'step': [
                    FBTABrowserConstant.DOING_CONTENT_CHECK_ONLY
                ]
            },
            'Join Facebook or log in to continue.': {
                'do': FBTABrowserConstant.STATUS_LOGIN_AGAIN,
                'step': [
                    FBTABrowserConstant.DOING_CONTENT_CHECK_ONLY
                ]
            },
            'Error Facebook': {
                'do': FBTABrowserConstant.STATUS_CONTENT_RELOAD_ONCE,
                'step': [
                    FBTABrowserConstant.DEBUG_SHOW_SOURCE,
                    FBTABrowserConstant.DOING_TITLE_CHECK_ONLY
                ]
            },
            'Content Not Found': {
                'do': FBTABrowserConstant.STATUS_SAVE_AND_IGNORE,
                'step': [
                    FBTABrowserConstant.DEBUG_SHOW_SOURCE,
                    FBTABrowserConstant.DOING_TITLE_CHECK_ONLY
                ]
            }

        }

    @property
    @abstractmethod
    def driver(self):
        raise NotImplementedError('Driver properties not implement')

    def set_tilte_driver(self, driver: webdriver.Chrome):
        self._driver = driver

    def detect_content_status(self, fbscope, contentcheck=False):
        result = []
        for key in self.__checker_login_tile:
            doing = self.__checker_login_tile.get(key).get('do')
            step = self.__checker_login_tile.get(key).get('step')
            if self.__has_someting_in_step(FBTABrowserConstant.DOING_TITLE_CHECK_ONLY, step):
                removed_word = str(self.driver.title).replace('| Facebook', '').lower().strip()
                if str(key).lower().strip() in removed_word:
                    result.append(doing)

            if self.__has_someting_in_step(FBTABrowserConstant.DOING_CONTENT_CHECK_ONLY, step):
                content = str(self.driver.page_source).lower().strip()
                if str(key).lower().strip() in content:
                    result.append(doing)

            if self.__has_someting_in_step(FBTABrowserConstant.DEBUG_SHOW_SOURCE, step):
                removed_word = str(self.driver.title).lower().strip()
                if str(key).lower().strip() in removed_word:
                    log('@DEBUG_SHOWSOURCE', self.driver.title, self.driver.raw_url)
                    with open('./Debug/debug_' + str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')) + '.log.txt',
                              mode='w', encoding='utf8') as fo:
                        fo.write(self.driver.raw_url)
                        fo.write('\n')
                        fo.write(self.driver.page_source)
        if result:
            return max(result)
        return FBTABrowserConstant.STATUS_NORMAL

    def __has_someting_in_step(self, checker, step):
        return any([checker == s for s in step])

    def check_login_type(self, fbscope):
        url = self.driver.current_url
        for key in self.__checker_login_url:
            if key in url:
                new_fbscope = self.__checker_login_url.get(key, fbscope)
                return (new_fbscope, True)
        return (fbscope, False)

    def checkNoCotent(self):
        tilte_str = 'Content Not Found'
        page_content_hasthis = 'The page you requested cannot be displayed right now.'
