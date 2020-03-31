import json
import os
import pickle
from pprint import pprint

import requests, re
from bs4 import BeautifulSoup
import html

from parsel import Selector


def add_cookies(session):
    file_name = './cookies/fbta_cookies_old.pkl'
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
    session = requests.Session()
    add_cookies(session)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }

    test_url = 'https://m.facebook.com/PixivNiconicoGazou/albums/2152919778138841/'
    test_url = 'https://m.facebook.com/pandetacademy/albums/3221380814570566'
    test_url = 'https://m.facebook.com/gianluca.rolli/albums/10218026786918731/'
    test_url = 'https://m.facebook.com/NonnaNyanNyan/photos/?tab=album&album_id=652802428527639&_rdr'
    test_url = 'https://m.facebook.com/1175443659329014'
    test_url = 'https://www.facebook.com/sirikran.lee/posts/876502709403361'   # POST X
    test_url = 'https://m.facebook.com/1559410897520563'   # images/single_post +22
    res = session.get(
        test_url,
        headers=headers)
    bs = BeautifulSoup(res.text, 'lxml')
    # f = bs.find_all('script')
    # print(bs)
    # print(f)
    sel = Selector(res.text)
    print(res.text)



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


