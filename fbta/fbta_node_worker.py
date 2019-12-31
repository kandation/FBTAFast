from time import sleep

# import fbta_util
import fbta_util
from fbta_browser_constant import FBTABrowserConstant
from fbta_browser_worker_new import FBTAWorkerBrowserS
from fbta_configs import FBTAConfigs
from fbta_node_master import FBTANodeMaster
from fbta_settings import FBTASettings
from fbta_url import FBTAUrl
from fbta_log import log


class FBTANodeWorker:
    NONE = None

    def __init__(self, slave_name: str, node_master: FBTANodeMaster):
        self.__node_master = node_master

        self.__settings = self.__node_master.settings
        self.__configs = self.__node_master.configs

        self.browser: FBTAWorkerBrowserS = FBTAWorkerBrowserS(self.__node_master)
        self.__run_browser()

        self.name = str(slave_name)

        self.__checkAginNewLoginIsOk = True

        self.__fbscrope: FBTABrowserConstant = FBTABrowserConstant.FBSCOPE_GLOBAL

    def setFBScope(self, scope):
        self.__fbscrope = scope

    def getSettings(self) -> FBTASettings:
        return self.__settings

    def getConfigs(self) -> FBTAConfigs:
        return self.__configs

    def auto_load_cookies(self):
        if self.__settings.init_node_master_browser:
            self.browser.driver.add_cookie_from_node_master()
        else:
            self.browser.driver.add_cookie_from_file()

    def run(self):
        if self.__settings.use_nodeSlave:
            self.__node_master.slave_waiting_node_master(self.name)
            log(f':Slave:\t\t\t[{self.name}] goto First Page')
            self.browser.goto(self.__node_master.url.getUrlFacebook())
            self.browser.load_cookies()
            self.browser.goto(self.__node_master.url.getUrlFacebook())

    def goto_Secure(self, url):
        try_loop = 0
        while True:
            self.browser.goto(url)
            if self.browser.has_signal_once:
                log(f':Slave: Has a signal once and dont GOTO URL')
                break

            if not self.browser.has_signal_loop or try_loop > 15:
                self.browser.reset_loop_signal()
                break

            self.__siteErrorHandling(url, try_loop)
        return True

    def __siteErrorHandling(self, url, try_loop):
        self.browser.fb_scope = self.__fbscrope
        if self.browser.login_signal:
            self.__node_master.slave_call_master_new_login(self, url)
            try_loop = 0
        if self.browser.signal_reload_content:
            log(':slave: Reload Content')
            sleep(10)
            try_loop += 1
        if self.browser.signal_reload_content:
            log(':slave: Reload Content')
            sleep(10)
            try_loop += 1
        if self.browser.signal_restart_browser:
            raise Exception('Kill Browser by exception for new instance browser')

    def screenshot_by_id(self, element_id: str, file_name: str, sub_dir=None):
        pass

    def screenshot_by_id_selenium(self, element_id: str, file_name: str, sub_dir=None):
        dir = self.__screenshot_check_directory(sub_dir)
        return self.__save_screenshot_by_id(element_id, file_name, dir)

    def screenshot_fullpage(self, file_name, sub_dir=None):
        pass

    def screenshot_fullpage_selenium(self, file_name, sub_dir=None):
        dir = self.__screenshot_check_directory(sub_dir)
        return self.__save_screenshot_fullpage(file_name, dir)

    def __save_screenshot_fullpage(self, file_name: str, dir: str):
        path = str(dir) + str(file_name) + '.png'
        try:
            if not fbta_util.fullpage_screenshot(self.browser.driver, path):
                log(f':Slave:\t\t\t> [{self.name}] save FULL_PAGE_SCREENSHOT NOT_SUCCESS at [{path}]')
                return False
            return True

        except Exception as e:
            log(f':Slave:\t\t\t> [{self.name}] Save FULL_PAGE_SCREENSHOT_ERROR at [{path}]')
        return False

    def __save_screenshot_by_id(self, element_id, file_name: str, dir: str):
        path = str(dir) + str(file_name) + '.png'
        try:
            if not fbta_util.screenshot_by_id(self.browser.driver, str(element_id), path):
                log(f':Slave:\t\t\t> [{self.name}] save SCREENSHOT_BY_ID NOT_SUCCESS at [{path}]')
                return False
            return True

        except Exception as e:
            log(f':Slave:\t\t\t> [{self.name}] save SCREENSHOT_BY_ID_ERROR at [{path}]')
        return False

    def __screenshot_check_directory(self, sub_dir=None):
        dir = str(self.__settings.dir_path)
        if sub_dir and sub_dir != '':
            dir += '/' + str(sub_dir)
        dir += '/'

        self.__screenshot_check_directory_make_chain(dir)
        return dir

    def __screenshot_check_directory_make_chain(self, dir):
        import os
        try:
            if not os.path.exists(dir):
                os.makedirs(dir)
        except:
            log(f':Slave:\t\t> Slave {self.name} Cannot Mkdirs Because Other Thread will created')

    def __del__(self):
        self.browser.killdriver()

    def __run_browser(self):
        if self.__settings.use_nodeSlave:
            self.browser.start_browser()
