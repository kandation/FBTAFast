import time

from fbta.fbta_log import log
from urllib.parse import unquote
from fbta.fbta_configs import FBTAConfigs
from fbta.fbta_driver import FBTADriver
from fbta.fbta_node_master import FBTANodeMaster
from fbta.fbta_settings import FBTASettings

from parsel import Selector
from pymongo import MongoClient
from urllib.parse import unquote

fb_url_m = 'https://m.facebook.com/'
fb_url_w = 'https://www.facebook.com/'

db_name = 'fbta_20200404_0432'


def url_fix(url):
    if 'http' not in url:
        t = 'https://m.facebook.com' + url
        return t
    return url

def is_http(url):
    return 'http' in url

from urllib.parse import urljoin
import html

def get_hops( url):
    import re as regex
    global session
    redirect_re = regex.compile('<meta[^>]*?url=(.*?)["\']', regex.IGNORECASE)
    hops = []
    while url:
        if url in hops:
            url = None
        else:
            hops.insert(0, url)
            response = session.get(url, True)
            if response.url != url:
                hops.insert(0, response.url)
            # check for redirect meta tag
            if response.encoding is not None:
                match = redirect_re.search(response.text)
                if match:
                    ref_url = match.groups()[0].strip()
                    if 'http' not in ref_url[:10]:
                        print('-----[Photo-Method] http not in ref url', ref_url)

                        url = urljoin(url, html.unescape(ref_url))
                    else:
                        url = html.unescape(ref_url)

                else:
                    url = None
            else:
                url = None
    return hops

def getName(url):
    import re as regex
    PATTERN = '([0-9]+_[0-9]+_[0-9]+_[on].[a-z]+)\?'
    tt = regex.findall(PATTERN, url)
    print(tt)
    tt = ''.join(tt)
    return tt

if __name__ == '__main__':
    settings = FBTASettings('fadehara')
    configs = FBTAConfigs()

    settings.kill_driver_on_end = True
    settings.driver_path = r'./Driver/chromedriver_76.exe'
    settings.dir_cookies = r'./cookies/'
    settings.use_nodeMaster_loadCookie = True

    settings.use_nodeMaster = False
    settings.init_node_master_browser = False

    settings.renew_index = False
    settings.fast_worker = True
    # settings.date_process = [2017, 10, 1]
    settings.dir_path_detail = settings.DIR_DETAIL_NEW_ALL_RUN

    node_master = FBTANodeMaster(settings, configs)
    node_master.start()

    session = FBTADriver(node_master)

    session.add_cookie_from_file()
    session.get('https://m.facebook.com')
    # session.delete_cookie('noscript')
    # session.set_header_chrome()
    session.set_header_firefox()

    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    # }

    page_error_topic = ['Content Not Found']

    client = MongoClient()
    db = client.get_database(db_name)
    # collection = db.get_collection('03_post_page')
    coll_album = db.get_collection('99_photos_tank')

    docs_post = coll_album.find()

    PHOTO_PATTERN = '\/([0-9]+)\/|\?fbid=([0-9]+)'

    url_patt = 'media/set/?set={a_type}.{aid}&type=1'
    allow_type = ['a', 'oa', 'pcb']


    for doc in docs_post:
        doc_url = doc.get('url')
        url = f'https://m.facebook.com{doc_url}'
        timer_download = time.time()

        source = session.get(url).text

        page_data = {
            'url': url,
            # 'cluster-history': self.name,
            'time': int(timer_download),
            'time-download': -1,
            'source': source
        }
        # int(time.time() - timer_download)

        link = Selector(source)
        px = link.xpath("//a[contains(.,'View Full Size')]").attrib.get('href')
        print('********' + px)

        if px:
            response = session.get(url_fix(px))

            if not is_http(px):
                lx = get_hops(url_fix(px))[0]
                nlink = unquote(lx)
                print('____________'+nlink)
                response = session.get(nlink)

            name = getName(response.url)

            if doc.get('type') != 'photo':
                name = f'a_{name}'

            print(name, end='\n\n')
        else:
            print(url)

        # if link:
        #     response = self.browser.goto(self.url_fix(link), stream=True)
        #
        #     if self.is_http(link):
        #         lk = self.__photos_method.get_hops(self.url_fix(link))[0]
        #         nlink = unquote(lk)
        #         print('+++++++++++++++++' + nlink)
        #         response = self.browser.goto(nlink, stream=True)
        #
        #     name = self.__getName(response.url)
        #
        #     if doc.get('type') != 'photo':
        #         name = f'a_{name}'
        #
        #     imgName = self.save_image_to_file(response, name)
        #     self.stat.add_stat('download_success')
        #     page_data['success'] = {
        #         'filename': imgName,
        #         'img-url': response.url,
        #         'header': str(response.headers),
        #         'org-link': link
        #     }
        #     page_data['time-download'] = time.time() - timer_download
        #     page_data = {'downloaded': page_data}
        #     self.__db.raw_collection_next().update_one({'_id': doc.get('_id')}, {'$set': page_data})
        #     del response
        #     return imgName
        # else:
        #     """
        #     WHEN DATA-FT IN DB IS OLDER POST WILL BE DELETED WHEN LOAD PAGE AGAIN FOUND NOT ELEMENTS
        #     """
        #     log(f':PDW: detect CONTENT_NOT_FOUND between download Photos @ {url}')
        #     self.stat.add_stat('download_fail')
        #     page_data['fail'] = url
        #     page_data['time-download'] = time.time() - timer_download
        #     page_data = {'downloaded': page_data}
        #     self.__db.raw_collection_next().update_one({'_id': doc.get('_id')}, {'$set': page_data})