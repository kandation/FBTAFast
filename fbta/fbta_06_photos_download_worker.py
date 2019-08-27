import re
import shutil
from typing import List, Optional

from fbta_06_photos_download_method import FBTAPhotosDownloadMethod
from fbta_global_database_manager import FBTADBManager
from fbta_03_history_download_method import FBTAHistoryDownloaderMethod
from fbta_main_worker import FBTAMainWorker
from fbta_node_master import FBTANodeMaster
from fbta_log import log


class FBTAPhotosDownloadWorker(FBTAMainWorker):
    def __init__(self, node_master: FBTANodeMaster, db: FBTADBManager):
        self.__node_master = node_master
        self.__db = db

        FBTAMainWorker.__init__(self, node_master)
        # self.__activity: FBTAHistoryDownloaderMethod = FBTAHistoryDownloaderMethod.NONE
        self.__photos_method:FBTAPhotosDownloadMethod = FBTAPhotosDownloadMethod.NONE

    def after_init(self):
        self.__photos_method = FBTAPhotosDownloadMethod(self.browser)
        pass
        # self.__activity = FBTAHistoryDownloaderMethod(self.__node_master, self.node_worker, self.__db)
        # self.__activity.slave_name = self.name

    def slave_method(self, docs):
        self.downloadSpliter(docs)

    def url_fix(self, url):
        if 'http' not in url:
            t = 'https://m.facebook.com' + url
            return t
        return url

    def is_http(self, url):
        return 'http' in url

    # TODO FIX FOUND All Cluster die to cancel download and end task
    def downloadSpliter(self, docsOnces):
        j = self.__photos_method.find_type_of_post(docsOnces)
        if j and j != '-1':
            url = self.__node_master.url.getUrlWithMain(j)
            self.browser.goto(url)
            # print('------------------')
            # TODO NOT secure get please use browser class
            link = self.browser.driver.selector.xpath("//a[contains(.,'View Full Size')]").attrib.get('href')
            if link:
                # TODO NOT secure get please use browser class
                # print('0000000',link)
                response = self.browser.goto(self.url_fix(link), stream=True)

                if not self.is_http(link):
                    # print(self.url_fix(link), response.status_code, response.history, response.headers)
                    lk = self.__photos_method.get_hops(self.url_fix(link))[0]
                    # print('111111111',lk)
                    # import urllib.parse
                    nlink = str(lk).replace('&amp;', '&')
                    # print('22222222',nlink)
                    response = self.browser.goto(nlink, stream=True)
                # print(response.json())

                name = self.__getName(response.url)
                # print(response.headers)
                # name = j
                # print('>>>>>>>>>>>>>>>>', name)
                imgName = self.save_image_to_file(response, name)
                self.stat.add_stat('download_success')
                del response
                return imgName
            else:
                """
                WHEN DATA-FT IN DB IS OLDER POST WILL BE DELETED WHEN LOAD PAGE AGIN FOUND NOT ELEMENTS
                """
                print(f':PDW: detect CONTENT_NOT_FOUND between download Photos @ {url}')
                self.stat.add_stat('download_fail')

    def __getName(self, url):
        tt = str(url).split('?_nc_')[0].split('/')[-1]
        return tt



    def save_image_to_file(self, image, name):
        names = '{dirname}/{suffix}'.format(
            dirname=self.__node_master.settings.getProjectPath(self.__node_master.configs.dir_seq_03_photos),
            suffix=name)
        with open(names, 'wb') as out_file:
            shutil.copyfileobj(image.raw, out_file)
        return names
