import time
from pprint import pprint

from fbta.fbta_04_activity_to_card import FBTAActivityToCardsNew
from fbta.fbta_05_cards_download_manager import FBTACardsDownloadManager
from fbta.fbta_02_clusters import FBTAClusterInfo
from fbta.fbta_06_photos_download_manager import FBTAPhotosDownloadManager
from fbta.fbta_07_dataft import FBTADataft
from fbta.fbta_090_01_album_preprocess import FBTA0901MoreAlbumPreProcess

from fbta.fbta_110_02_user_info import FBTA11001UserInfo
from fbta.fbta_110_03_user_info_album import FBTA11001UserInfoAlbum
from fbta.fbta_120_00_cal_count_number import FBTA120CountingAlbumPreprocess
from fbta.fbta_140_album_other_survey_manager import FBTA140AlbumOtherSurvey
from fbta.fbta_150_more_album_preprocess import FBTA150MoreAlbumPreProcess
from fbta.fbta_configs import FBTAConfigs
from fbta.fbta_03_history_download_manager import FBTAHistoryDownloadManager
from fbta.fbta_mkdir import FBTAMkdir
from fbta.fbta_node_master import FBTANodeMaster
from fbta.fbta_sequence_func import FBTASequenceFunction
from fbta.fbta_settings import FBTASettings
from fbta.fbta_01_yearbox import FBTAYearBox
from fbta.fbta_log import log


class FBTASequenceNew(FBTASequenceFunction):
    def __init__(self, setting: FBTASettings, configs: FBTAConfigs):
        FBTASequenceFunction.__init__(self, setting, configs)

        self.__dir_path = setting.dir_path

        self.__node_master: FBTANodeMaster = FBTANodeMaster.NONE

        self.__node_year_box = None
        self.__node_cluster_info: FBTAClusterInfo = None

    def start(self):
        log(f'$START_FBTA_TEST$_&/{self.__dir_path}')
        self._warnningTimeOptimize()
        self.__px0_initDirectory()

        self.__save_information()

        step_function = [
            self.__p00_generateMasterNode,
            self.__p01_net_single__year_box,
            self.__p02_db__single__cal_cluster_info,
            self.__p03_net_cluster_download_activity_all,
            self.__p04_db__single__transfer_activity_to_story_card,
            self.__p05_net_cluster_download_story,
            self.__parse_photo_in_story_trans_to_photo_id_and_data_ft,
            self.__p07_create_album_no_dup,
            self.__p08_create_photo_tank_no_dup,
            self.__p09_download_first_page_album,
            self.__p09_01_parse_first_page_to_photo,
            self.__p10_create_photo_tank_from_album,
            self.__p12_download_story_as_chrome,
            self.__p11_02_user_info_album_with_chrome_header,
            self.__p12_counting_album_preprocess,
            # self.__p140_00_cluster_download_more_album_page,
            # self.__p150_00_parse_more_album_page_and_add_photo_to_tank,
            self.__p11_01_user_info_make_all_ignore_case,
            self.__p11_processEazyPhotoDownload,
            # FBTA COMPLETE YOU GET ALL PHOTO FROM YOU LIKE
        ]
        """
        TODO: 630423 - โหลดวีดีโอ, โหลดรูปจากลิงก์, รูปภาพสามมิติที่คล้ายลิงก์ แต่ไม่มีข้อความ และมีภาพเต็ม
        TODO: 630423 - Clean Code, Websocket Log, UI
        """

        for index, func in enumerate(step_function):
            if self._isInTestStep(index):
                func()
            self._showFinishedProcessEndNotify(index)

        print('ENDT$EST')
        

    def __px0_initDirectory(self):
        self.__mkdirClass = FBTAMkdir(self._settings, self._configs)
        self.__mkdirClass.startProjectDir()

    def __p00_generateMasterNode(self):
        self.__node_master = FBTANodeMaster(self._settings, self._configs)
        self.__node_master.start()

    def __p01_net_single__year_box(self):
        self.__node_year_box = FBTAYearBox(self.__node_master)
        self.__node_year_box.run()

    def __p02_db__single__cal_cluster_info(self):
        self.__node_cluster_info = FBTAClusterInfo(self._settings, self._configs, self.__node_year_box)
        self.__node_cluster_info.run()

    def __p03_net_cluster_download_activity_all(self):
        # Step01 Download Activity
        dl = FBTAHistoryDownloadManager(self.__node_master,
                                        self.__node_cluster_info.clusters)
        dl.main()

    def __p04_db__single__transfer_activity_to_story_card(self):
        analysis = FBTAActivityToCardsNew(self._settings, self._configs)
        analysis.main()

    def __p05_net_cluster_download_story(self):
        order = FBTACardsDownloadManager(self.__node_master)
        order.main()

    def __parse_photo_in_story_trans_to_photo_id_and_data_ft(self):
        import fbta.fbta_060_00_album_parse
        fbta.fbta_060_00_album_parse.main(self.__node_master.settings.db_name)

    def __p09_download_first_page_album(self):
        from fbta.fbta_090_00_album_single_surway_manager import FBTA090AlbumSingSurvey
        album_surway = FBTA090AlbumSingSurvey(self.__node_master)
        album_surway.main()

    def __p09_01_parse_first_page_to_photo(self):
        album_surway = FBTA0901MoreAlbumPreProcess()
        album_surway.main(self.__node_master.settings.db_name)

    def __p07_create_album_no_dup(self):
        import fbta.fbta_070_00_create_no_duplicate_album
        fbta.fbta_070_00_create_no_duplicate_album.main(self.__node_master.settings.db_name)

    def __p08_create_photo_tank_no_dup(self):
        import fbta.fbta_080_00_create_no_duplicate_photo
        fbta.fbta_080_00_create_no_duplicate_photo.main(self.__node_master.settings.db_name)

    def __p10_create_photo_tank_from_album(self):
        import fbta.fbta_100_00_create_photo_from_album
        fbta.fbta_100_00_create_photo_from_album.main(self.__node_master.settings.db_name)

    def __p11_processEazyPhotoDownload(self):
        from fbta.fbta_110_00_photos_download_manager import FBTA11000PhotosDownloadManager
        dl = FBTA11000PhotosDownloadManager(self.__node_master)
        dl.main()

    def __p12_download_story_as_chrome(self):
        order = FBTACardsDownloadManager(self.__node_master, step_find_album_count=True)
        order.main()

    def __p12_counting_album_preprocess(self):
        counter = FBTA120CountingAlbumPreprocess()
        counter.main(self.__node_master.settings.db_name)

    def __p11_01_user_info_make_all_ignore_case(self):
        user_info = FBTA11001UserInfo()
        user_info.main(self.__node_master.settings.db_name,
                       self.__node_master.settings.ignore_names)

    def __p11_02_user_info_album_with_chrome_header(self):
        user_info = FBTA11001UserInfoAlbum()
        user_info.main(self.__node_master.settings.db_name,
                       self.__node_master.settings.ignore_names)

    def __p140_00_cluster_download_more_album_page(self):
        user_info = FBTA140AlbumOtherSurvey(self.__node_master)
        user_info.main()

    def __p150_00_parse_more_album_page_and_add_photo_to_tank(self):
        user_info = FBTA150MoreAlbumPreProcess()
        user_info.main(self.__node_master.settings.db_name)

    def __save_information(self):
        from pymongo import  MongoClient
        client = MongoClient()
        db = client.get_database(self._settings.db_name)
        coll = db.get_collection('information')
        coll.insert_one(self._settings.get_json_setting())
