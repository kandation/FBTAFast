from fbta_configs import FBTAConfigs
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
    settings.date_process = [2019, 7, 1]
    settings.dir_path_detail = settings.DIR_DETAIL_NEW_ALL_RUN

    seq = FBTASequence(settings, configs)
    seq.start()
