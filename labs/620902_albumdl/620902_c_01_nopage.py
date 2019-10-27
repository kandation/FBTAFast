"""
No 'page_insights' คืออัลบัมที่ไม่ได้โพสโพยเพจ
ถึงจะเป็น Album หรือ PhotoGroup ก็ตาม ควรใช้การ parse หาว่ามีชื่ออัลบัมแทนดีกว่า
การใช้ requests สำหรับวิธีรี้จะยากเกินไป (ความอดทนต่ำ) แนะนำให้ใช้ process แบบใหม่
- เมื่อรู้ว่าอัลบัมนี้มีภาพจำนวนเท่าไรแล้ว ถ้าม > 1000 ให้ใช้ selenium เข้ามาเก็บรูปภาพแทน
- ถ้าน้อยกว่า (ส่วนใหญ่ก็น้อยกว่าอยู่แล้ว) ก็ให้ใช้ เดินตามลิงก์โง่ๆเลย


"""

from bs4 import BeautifulSoup
import os
import pickle
import requests, re
from bs4 import BeautifulSoup
import html

from parsel import Selector
def add_cookies(session):
    file_name = 'cookies/fbta_cookies_old.pkl'
    if os.path.exists(file_name):
        cookies = pickle.load(open(file_name, mode='rb'))
        for cookie in cookies:
            if cookie['name'] != 'noscript':
                session.cookies.set(cookie['name'], cookie['value'])

if __name__ == '__main__':
    session = requests.Session()
    add_cookies(session)

    headers = {
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
    }
    #
    # url = "https://touch.facebook.com/media/set/?set=oa.2970320783192191"
    #
    #
    # res = session.get(
    #     url,
    #     headers=headers)
    # bs = BeautifulSoup(res.text, 'lxml')
    # print(res.encoding)
    # exit()
    #
    # with open('soft_ff.html', mode='w', encoding=res.encoding) as fo:
    #     fo.write(res.text)
    # exit()

    ##### FAIL RESULT อย่าทำต่อเลย เสียเวลา กลับไปใช้งานเดิมดีกว่า

    with open('soft_ff.html', mode='r', encoding='utf-8') as fo:
        data = fo.read()
    sel = Selector(data)
    # scripts = bs.find_all('div.hidden_elem')
    scripts = sel.xpath('//script')
    for i,tx in enumerate(scripts.getall()):
        if 'ajaxResponseTo' in tx:
            print(i,',')
        if 'USER_ID' in tx:
            print(i,',')
        if 'dtsg_ag' in tx:
            print(i,',')
    new_str = str(scripts[11].xpath('text()').get())
    param = {
        'user_id':0,
        'ajax':0,
        'dtsg_ag':0
    }
    print(new_str[new_str.find('"USER_ID"'):new_str.find('"USER_ID"')+50])

    REG = '(?:"USER_ID":")(.*?)(?:",")'
    kk = re.findall(REG, new_str)
    param['user_id'] = kk[0]

    REG = '(?:"encrypted":")(.*?)(?:"})'
    kk = re.findall(REG, new_str)
    param['ajax'] = kk[0]
    REG = '(?:"dtsg_ag":{"token":")(.*?)(?:",)'
    # dtsg_ag
    kk = re.findall(REG, new_str)
    param['dtsg_ag'] = kk[0]

    print(param)

    url_home  = 'https://touch.facebook.com/home.php?__m_async_page__=&__big_pipe_on__=&m_sess=&fb_dtsg_ag={0}&__req=1&__ajax__={1}&__a={1}&__user={2}'
    url_home = url_home.format(param['dtsg_ag'],param['ajax'],param['user_id'])

    res = session.get(
        url_home,
        headers=headers)

    with open('soft_kk.html', mode='w', encoding=res.encoding) as fo:
        fo.write(res.text)
    with open('soft_kk.html', mode='r', encoding=res.encoding) as fo:
        result = fo.read()

    print(result)
    # result = res.text
    result = str(result).replace('for (;;);','')

    result = str(result).replace('false','false')
    result = str(result).replace('true','true')
    # print(result)
    # py_obj = eval(result)
    import demjson

    # from
    # js_obj = '{x:1, y:2, z:3}'

    # to
    py_obj = demjson.decode(result)
    # k = py_obj['domops'][0][3]['__html']
    print(py_obj)
    # bs = BeautifulSoup(py_obj, 'lxml')
    # print(bs.prettify())
    exit()

    with open('labs/620902_albumdl/test_case/6209021742_timeline.js', mode='r') as fo:
        data = fo.read()

    js_obj =data

    import demjson

    # from
    # js_obj = '{x:1, y:2, z:3}'

    # to
    py_obj = demjson.decode(js_obj)
    k = py_obj['domops'][0][3]['__html']
    print(k)
    bs =BeautifulSoup(k,'lxml')
    print(bs.prettify())

