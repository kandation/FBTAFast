from fbta.fbta_configs import FBTAConfigs
from fbta.fbta_log import log
from fbta.fbta_sequence_new import FBTASequenceNew
from fbta.fbta_settings import FBTASettings
import multiprocessing


if __name__ == '__main__':
    # settings = FBTASettings('fadehara')
    settings = FBTASettings('kanda.kiesekun')
    configs = FBTAConfigs()

    settings.kill_driver_on_end = True
    settings.driver_path = r'./Driver/chromedriver_84.exe'
    settings.dir_cookies = r'./cookies/'
    settings.dir_save_path = r'../save/'
    settings.use_nodeMaster_loadCookie = True
    settings.use_nodeMaster = True
    settings.init_node_master_browser = True
    settings.cluster_num = multiprocessing.cpu_count()
    settings.cluster_limit = 50
    # settings.headerless = True

    settings.renew_index = True
    settings.fast_worker = True

    settings.json_cookie = True

    # settings.date_process = [2018, 7, 1]
    # settings.date_process = [2019, 8, 1]
    # settings.date_process = [2019, 10, 1]
    # settings.date_process = [2020, 1, 1]
    # settings.date_process = [2020, 5, 1]
    settings.date_process = [2020, 10, 1]
    settings.dir_path_detail = settings.DIR_DETAIL_NEW_ALL_RUN

    settings.description = 'เก็บงานของเดือนนี้ และพยายามให้เฟสบุ๊คแบน [firefox]'
    settings.description = 'จะพยายามหารายชื่อเพจทั้งเคยกดไลค์เพื่อย้ายแอค'
    settings.description = 'เก็บงานทั้งหมดก้วย kieseki 630914'
    settings.description = 'ทดสอบเขียนด้วย vscode'
    # settings.db_name = 'fbta_20190827_1544'
    # settings.db_name = 'fbta_20190906_1220'
    # settings.db_name = 'fbta_20191029_0138'
    # settings.db_name = 'fbta_20191030_0259'
    # settings.db_name = 'fbta_20191114_1901'
    # settings.db_name = 'fbta_20200202_1816'
    # settings.db_name = 'fbta_20200226_1437'
    # settings.db_name = 'fbta_20200404_1650'
    # settings.db_name = 'fbta_20200405_0314'
    # settings.db_name = 'fbta_20200404_1650'
    # settings.db_name = 'fbta_20200407_2208'
    # settings.db_name = 'fbta_20200422_0329'
    # settings.db_name = 'fbta_20200427_1436'
    # db = client.get_database('fbta_20190827_1544')
    # db = client.get_database('fbta_20190827_1544')
    # db = client.get_database('fbta_20190619_0031')
    # db = client.get_database('fbta_20190827_2027')

    # settings.test_step = [0, 5, 6]
    # settings.test_step = [0,1,2,3,4,5]
    # settings.test_step = [0, 11]
    # settings.test_step = [0, 1,2,3,4]
    # settings.test_step = [0,15]
    # settings.test_step = [0,1,2,3,4,5]
    # settings.test_step = [0,1,2,3,4]
    # settings.test_step = [0, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    # settings.use_resume = True

    seq = FBTASequenceNew(settings, configs)
    seq.start()
