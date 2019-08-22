from fbta_browser_fast import FBTABrowserFastDriver
from fbta_configs import FBTAConfigs
from fbta_node_master import FBTANodeMaster
from fbta_sequence import FBTASequence
from fbta_settings import FBTASettings

if __name__ == '__main__':
    settings = FBTASettings('fadehara')
    configs = FBTAConfigs()

    settings.kill_driver_on_end = True
    settings.driver_path = r'./Driver/chromedriver_76.exe'
    settings.dir_cookies = r'./cookies/'
    settings.use_nodeMaster_loadCookie = True
    settings.use_nodeMaster = True

    settings.renew_index = False
    settings.fast_worker = True
    settings.date_process = [2017, 10, 1]
    settings.dir_path_detail = settings.DIR_DETAIL_NEW_ALL_RUN
    settings.use_nodeMaster = True

    node_master  = FBTANodeMaster(settings, configs)
    node_master.start()

    re = FBTABrowserFastDriver(node_master)
    # re.start_session()
    # re.add_cookie_from_file()
    re.get('https://m.facebook.com')
    print(re.current_url)
    print(re.page_source)
    print(re.get_cookies())
    print(re.title())
    print(re.find_element_by_name('email'))
    # re.add_cookie_from_file()
    re.add_cookie_frome_node_master()
    re.get('https://m.facebook.com/me')
    print(re.title())
    print(re.find_element_by_xpath('//div[@id="m-timeline-cover-section"]'))
