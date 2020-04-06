import re
import shutil
import time
from typing import List, Optional

from fbta_110_00_photos_download_method import FBTA11000PhotosDownloadMethod
from fbta_browser_constant import FBTABrowserConstant
from fbta_global_database_manager import FBTADBManager
from fbta_03_history_download_method import FBTAHistoryDownloaderMethod
from fbta_main_worker import FBTAMainWorker
from fbta_node_master import FBTANodeMaster
from fbta_log import log

from urllib.parse import unquote


class FBTA11000PhotosDownloadWorker(FBTAMainWorker):
    def __init__(self, node_master: FBTANodeMaster, db: FBTADBManager):
        self.__node_master = node_master
        self.__db = db

        FBTAMainWorker.__init__(self, node_master)
        self.__photos_method: FBTA11000PhotosDownloadMethod = FBTA11000PhotosDownloadMethod.NONE

    def after_init(self):
        self.__photos_method = FBTA11000PhotosDownloadMethod(self.browser)

    def slave_method(self, docs):
        self.easy_download(docs)

    def url_fix(self, url):
        if 'http' not in url:
            t = 'https://m.facebook.com' + url
            return t
        return url

    def is_http(self, url):
        return 'http' in url

    def easy_download(self, doc):
        doc_url = doc.get('url')
        url = f'https://m.facebook.com{doc_url}'
        self.browser.goto(url)
        timer_download = time.time()

        source = self.browser.driver.page_source

        page_data = {
            'url': url,
            'cluster-history': self.name,
            'time': int(timer_download),
            'time-download': -1,
            'source': source
        }
        # int(time.time() - timer_download)

        link = self.browser.driver.selector.xpath("//a[contains(.,'View Full Size')]").attrib.get('href')

        if link:
            response = self.browser.goto(self.url_fix(link), stream=True)

            if not self.is_http(link):
                lk = self.__photos_method.get_hops(self.url_fix(link))[0]
                nlink = unquote(lk)
                print('+++++++++++++++++' + nlink)
                response = self.browser.goto(nlink, stream=True)

            name = self.__getName(response.url)

            if doc.get('type') != 'photo':
                aid = doc.get('aid', '')
                name = f'a_{aid}_{name}'

            imgName = self.save_image_to_file(response, name)

            self.stat.add_stat('download_success')
            page_data['success'] = {
                'filename': imgName,
                'img-url': response.url,
                'header': str(response.headers),
                'org-link': link
            }
            page_data['time-download'] = time.time() - timer_download
            page_data = {'downloaded': page_data}
            self.__db.raw_collection_next().update_one({'_id': doc.get('_id')}, {'$set': page_data})
            del response
        else:
            """
            WHEN DATA-FT IN DB IS OLDER POST WILL BE DELETED WHEN LOAD PAGE AGAIN FOUND NOT ELEMENTS
            """
            page_data['fail'] = {'url': url, 'type': 'video'}
            if self.browser.get_browser_status() == FBTABrowserConstant.STATUS_SAVE_AND_IGNORE:
                log(f':PDW: detect CONTENT_NOT_FOUND between download Photos @ {url}')
                page_data['fail']['type'] = 'CONTENT_NOT_FOUND'
            self.stat.add_stat('download_fail')
            page_data['time-download'] = time.time() - timer_download
            page_data = {'downloaded': page_data}
            self.__db.raw_collection_next().update_one({'_id': doc.get('_id')}, {'$set': page_data})
        self.__db.raw_collection_current().update_one({'_id': doc.get('_id')}, {'$set': self.__db.get_resume_key()})

    def __getName(self, url):
        import re as regex
        PATTERN = '([0-9]+_[0-9]+_[0-9]+_[on].[a-z]+)\?'
        tt = regex.findall(PATTERN, url)
        print(tt)
        tt = ''.join(tt)
        return tt

    def save_image_to_file(self, image, name):
        names = '{dirname}/{suffix}'.format(
            dirname=self.__node_master.settings.getProjectPath(self.__node_master.configs.dir_seq_03_photos),
            suffix=name)
        with open(names, 'wb') as out_file:
            shutil.copyfileobj(image.raw, out_file)
        return names
