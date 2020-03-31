import json
import os
import pickle
from pprint import pprint

import requests, re
from bs4 import BeautifulSoup
import html

from parsel import Selector

from fbta_configs import FBTAConfigs
from fbta_driver import FBTADriver
from fbta_node_master import FBTANodeMaster
from fbta_settings import FBTASettings


def add_cookies(session):
    file_name = './cookies/fbta_cookies.pkl'
    if os.path.exists(file_name):
        cookies = pickle.load(open(file_name, mode='rb'))
        for cookie in cookies:
            if cookie['name'] != 'noscript':
                session.cookies.set(cookie['name'], cookie['value'])

if __name__ == '__main__':
    """
    FBAlbumDownloader Labs Version @620829
    """
    images = []

    fb_url_w = 'https://www.facebook.com'

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
    settings.date_process = [2017, 10, 1]
    settings.dir_path_detail = settings.DIR_DETAIL_NEW_ALL_RUN

    node_master = FBTANodeMaster(settings, configs)
    node_master.start()

    session = FBTADriver(node_master)

    session.add_cookie_from_file()
    session.get('https://m.facebook.com')
    # session.delete_cookie('noscript')
    # session.set_header_chrome()


    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }

    test_url = 'https://m.facebook.com/PixivNiconicoGazou/albums/2152919778138841/'
    test_url = 'https://m.facebook.com/pandetacademy/albums/3221380814570566'
    test_url = 'https://m.facebook.com/gianluca.rolli/albums/10218026786918731/'
    test_url = 'https://m.facebook.com/NonnaNyanNyan/photos/?tab=album&album_id=652802428527639&_rdr'
    test_url = 'https://m.facebook.com/1175443659329014'

    res = session.get(test_url)
    bs = BeautifulSoup(res.text, 'lxml')
    # print(res.text)
    # f = bs.find_all('script')
    # print(bs)
    # print(f)
    print(res.text)
    sel = Selector(res.text)



    a_all_first = sel.xpath('.//div[@id="pages_msite_body_contents"]')
    ppp = a_all_first.xpath('.//a[@href and contains(@href,"photos")]')

    if len(ppp) == 0:
        # Case :'https://m.facebook.com/gianluca.rolli/albums/10218026786918731/'
        # Mean they upload each n images not album
        pass

    for ppa in ppp:
        images.append(ppa.attrib.get('href'))
    # print((images))

    REG = '(?:href:")(.*?)(?:")'
    p = re.findall(REG, str(res.text))
    if p:
        p = p.pop()
        print(p)
        while True:
            res = session.get(
                'https://m.facebook.com/'+p,
                headers=headers)
            text = str(res.text).replace('for (;;);', '')
            # print(text)
            text = text.replace('false', 'False')
            text = text.replace('true', 'True')
            py = eval(text)
            k = py['payload']['actions'][0]['html']
            hh = str(k).replace('\\','')

            # print(hh)

            bs = BeautifulSoup(hh, 'lxml')
            a_all = bs.find_all('a')
            for aa in a_all:
                images.append(aa['href'])

            REG = '(?:"href":")(.*?)(?:")'
            if len(py['payload']['actions']) < 3:
                # No cmd: script
                break
            k = html.unescape(py['payload']['actions'][2]['code'])
            p = re.findall(REG, str(k))
            p = str(p[0].encode().decode('unicode_escape')).replace('\\', '')
            print(p)

    print(len(images))

