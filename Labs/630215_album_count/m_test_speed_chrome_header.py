import time, statistics

from fbta_browser_worker import FBTADriver
from fbta_configs import FBTAConfigs
from fbta_node_master import FBTANodeMaster
from fbta_settings import FBTASettings
import parsel


def pp(url, stream=False):
    st = time.time()
    re.get(url,show_url=False,stream=stream)
    fin = time.time()
    return fin - st

def average_geturl(url, t=10, stream=False):
    timer_loop = []
    for _ in range(t):
        a = pp(url, stream=stream)
        # print(a)
        timer_loop.append(a)
    print(f'AVR={statistics.mean(timer_loop)}')

def save_html(fname, data):
    with open(f'./{fname}.html', mode='w', encoding='utf8') as fo:
        fo.write(data)

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
    settings.date_process = [2017, 10, 1]
    settings.dir_path_detail = settings.DIR_DETAIL_NEW_ALL_RUN

    node_master = FBTANodeMaster(settings, configs)
    node_master.start()

    re = FBTADriver(node_master)



    re.start_session()
    re.add_cookie_from_file()
    re.get('https://m.facebook.com')
    """
        การทดสอบหา url ที่เร็วที่สุดและดีที่สุด
        ผลคือ m.facbook.com/story แบบ noscript+python user-agent เร็วสุุด
        แม้ใกล้ๆกันจะมี m.facebook.com/user/post/a:b ซึ่งบางที่เร็วกว่า บางที่ช้ากว่า ไม่เสถียร
        --------
        ส่วนการจะหา album count ยอมแพ้ไปเถอะ ใช้หน้าโหลดเร็วสุด 1 วิ จาก noscript+user-agent:* แต่จะ phrase เนื้อหายากมาก
        m.fb/user หรือ story ใช้ 3 วิ ช้ามาก แต่หา data-ft ง่าย
        ส่วน touch.f เป็นแบบ lazy load กากมาก นึกว่าขยะสด 
        --------
        คำแนะนำสำหรับการทำ album count คือ
        ใช้แบบ 0.33 วิเพื่อเก็บข้อมูลมาวิเคราะห์เถอะ เพราะรูปภาพ 1/10 ถ้าใช้ 3 วิ มันเกินไป ยังไม่รวมพวก ลิงค์โง่ๆอีก
        อ่านต่อใน 620825 daraft_parse
        ------
    """
    # for iii in range(5):
    #     url_test = 'https://m.facebook.com/story.php?story_fbid=3062224330477381&substory_index=89&id=100000695314425'
    #     # url_test = 'https://m.facebook.com/fadehara/posts/3062224330477381:89'
    #     # url_test = 'https://www.facebook.com/fadehara/posts/3062224330477381:89'
    #     # re.delete_cookie('noscript')
    #     average_geturl(url_test, 10)
    #
    #     # re.get(url_test)
    #     # save_html('story_python', re.page_source)
    #     # print(re.session.headers)
    #
    #     url_test = 'https://m.facebook.com/fadehara/posts/3062224330477381:89'
    #     average_geturl(url_test, 10)
    #     print('-'*50)
    #     # exit()


    """
    การจะหา album count วิธีที่ดีที่สุดคือ www-url ลบ no-script ทิ้ง จะใช้ header ของใครก็ได้
    แนะนำ chrome/firefox จากนั้นทำงาน pasre html ด้วยคลาส hidden_elem เพื่อปล๊ดคอมเม้น
    แต่จะลองใช้ (?<=[\>])(\+[0-9]+)(?=[\<]) เพื่อเอาเฉพาะตัวเลขก็ได้
    """

    url_test = 'https://www.facebook.com/story.php?story_fbid=3062224330477381&substory_index=89&id=100000695314425'
    # url_test = 'https://www.facebook.com/story.php?story_fbid=3181054815260998&substory_index=1&id=100000695314425'
    # url_test = 'https://www.facebook.com/story.php?story_fbid=2071698746196616&substory_index=0&id=100000695314425'

    re.delete_cookie('noscript')
    re.set_header_chrome()
    # re.set_header_firefox()
    # headers_opera = {'user-agent':'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'}
    # re.set_headers_custome(headers_opera)
    average_geturl(url_test, 10)
    re.get(url_test)
    # print(re.session.headers)
    print(re.get_headers())
    # print(re.get_cookies())
    # # print(re.current_url)
    # # print(re.page_source)
    # # print(re.get_cookies())
    # # print(re.title)
    # # print(re.find_element_by_name('email'))
    # # re.add_cookie_from_file()
    # print('--------' * 10)
    # # re.add_cookie_from_node_master()
    # re.get('https://m.facebook.com/me')
    # print(re.title)
    # # print(re.find_element_by_xpath('//div[@id="m-timeline-cover-section"]'))
    # # re.get('https://m.facebook.com/me/allactivity')
    # # print(re.title)
    # # print(re.find_elements_by_xpath('//div[contains(@id, "month_") and not(contains(@id, "_more_"))]'))
    # # print(re.selector.css('#viewport'))
    #
    # # average_geturl('https://m.facebook.com/me',100)
    # # average_geturl('https://m.facebook.com/story.php?story_fbid=3016328265066988&substory_index=112&id=100000695314425',100)
    # # average_geturl('https://www.facebook.com/fadehara/posts/3016328265066988:112',100)
    # #

    # re.get('https://m.facebook.com/story.php?story_fbid=3062224330477381&substory_index=89&id=100000695314425')
    # print(re.session.headers)

    # """
    # Paser Album Couter
    # นี่เป็นแค่ตัวหาอัลบัม สามารถใช้แทน story download ได้เลย เพราะมันหา data-ft อยู่แล้ว แต่ที่ได้ก่อน
    # คือ จำนวนภาพในอัลบัม จะได้ไม่ต้องไปหาขั้นตอนอื่นอีกที่ แต่ต้องชั้งใจดูเวลา พอใส่แล้วจะทำให้ Node เวลาเพิ่มเปล่า
    # """
    # # TODO ปรับแต่งให้อ่าน data-ft
    # with open('./story.html', mode='r', encoding='utf8') as fo:
    #     data  = fo.read()
    # ps = parsel.Selector(data)
    # k =ps.xpath('//code').get(0)
    # fs = str(k).find('<!--')
    # print(str(k)[fs+4:-10].strip())
    #
    # ps = parsel.Selector(str(k)[fs+4:-10].strip())
    # k =ps.xpath('//div[contains(@class, "story")]')[0]
    # k=k.xpath('./div[2]/descendant-or-self::a')
    # for ii in k:
    #     print(ii.xpath('.//text()'))

    # k = re.selector.xpath('//div[contains(@class, "story") ')
    # print(k)
    save_html('story2',re.page_source)
