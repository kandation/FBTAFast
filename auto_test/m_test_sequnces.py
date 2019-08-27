from fbta_configs import FBTAConfigs
from fbta_sequence import FBTASequence
from fbta_settings import FBTASettings

if __name__ == '__main__':
    settings = FBTASettings('fadehara')
    configs = FBTAConfigs()

    settings.kill_driver_on_end = True
    settings.driver_path = r'./Driver/chromedriver_76.exe'
    settings.dir_cookies = r'./cookies/'
    settings.dir_save_path = r'./save/'
    settings.use_nodeMaster_loadCookie = True
    settings.use_nodeMaster = True
    settings.init_node_master_browser = False
    settings.cluster_num = 50
    settings.cluster_limit = 50

    settings.renew_index = False
    settings.fast_worker = True
    # settings.date_process = [2018, 7, 1]
    settings.date_process = [2019, 7, 1]
    settings.dir_path_detail = settings.DIR_DETAIL_NEW_ALL_RUN
    settings.db_name = 'fbta_20190825_1941'

    settings.test_step = [0,6]

    seq = FBTASequence(settings, configs)
    seq.start()
