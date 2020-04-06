import time, statistics

from fbta_browser_worker import FBTADriver
from fbta_configs import FBTAConfigs
from fbta_node_master import FBTANodeMaster
from fbta_settings import FBTASettings


def pp(url):
    st = time.time()
    re.get(url,show_url=False)
    fin = time.time()
    return fin - st

def average_geturl(url, t=10):
    timer_loop = []
    for _ in range(t):
        a = pp(url)
        # print(a)
        timer_loop.append(a)
    print(f'AVR={statistics.mean(timer_loop)}')


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
    # re.start_session()
    # re.add_cookie_from_file()
    re.get('https://m.facebook.com')
    # print(re.current_url)
    # print(re.page_source)
    # print(re.get_cookies())
    # print(re.title)
    # print(re.find_element_by_name('email'))
    re.add_cookie_from_file()
    print('--------' * 10)
    # re.add_cookie_from_node_master()
    re.get('https://m.facebook.com/me')
    print(re.title)
    # print(re.find_element_by_xpath('//div[@id="m-timeline-cover-section"]'))
    # re.get('https://m.facebook.com/me/allactivity')
    # print(re.title)
    # print(re.find_elements_by_xpath('//div[contains(@id, "month_") and not(contains(@id, "_more_"))]'))
    # print(re.selector.css('#viewport'))

    average_geturl('https://m.facebook.com/1559410897520563',100)



