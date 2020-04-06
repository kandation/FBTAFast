import time
from pprint import pprint

from fbta_04_activity_to_card import FBTAActivityToCardsNew
from fbta_05_cards_download_manager import FBTACardsDownloadManager
from fbta_02_clusters import FBTAClusterInfo
from fbta_06_photos_download_manager import FBTAPhotosDownloadManager
from fbta_07_dataft import FBTADataft
from fbta_120_album_count_manager import FBTAAlbumCountManager
from fbta_configs import FBTAConfigs
from fbta_03_history_download_manager import FBTAHistoryDownloadManager
from fbta_mkdir import FBTAMkdir
from fbta_node_master import FBTANodeMaster
from fbta_sequence_func import FBTASequenceFunction
from fbta_settings import FBTASettings
from fbta_01_yearbox import FBTAYearBox
from fbta_log import log


class FBTASequenceNew(FBTASequenceFunction):
    def __init__(self, setting: FBTASettings, configs: FBTAConfigs):
        FBTASequenceFunction.__init__(self, setting, configs)

        self.__dir_path = setting.dir_path

        self.__node_master: FBTANodeMaster = FBTANodeMaster.NONE

        self.__node_yearbox = None
        self.__node_cluster_info: FBTAClusterInfo = None

    def start(self):
        log(f'$START_FBTA_TEST$_&/{self.__dir_path}')
        self._warnningTimeOptimize()
        self.__px0_initDirectory()

        step_function = [
            self.__p00_generateMasterNode,
            self.__p01_processYearBox,
            self.__p02_processsClustersInfo,
            self.__p03_processDownloader,
            self.__p04_processDatabaseAsCard,
            self.__p05_processCardAsPost,
            self.__processAlbumParse,
            self.__p07_crate_album,
            self.__p08_crate_photo,
            self.__p09_processSingleAlbum,
            self.__p10_crate_photo_from_album,
            self.__p11_processEazyPhotoDownload
        ]

        for index, func in enumerate(step_function):
            func(index)
            self._showFinishedProcessEndNotify(index)

        print('ENDT$EST')
        exit()

    def __px0_initDirectory(self):
        self.__mkdirClass = FBTAMkdir(self._settings, self._configs)
        self.__mkdirClass.startProjectDir()

    def __p00_generateMasterNode(self, step):
        if self._isInTestStep(step):
            self.__node_master = FBTANodeMaster(self._settings, self._configs)
            self.__node_master.start()

    def __p01_processYearBox(self, step):
        if self._isInTestStep(step):
            self.__node_yearbox = FBTAYearBox(self.__node_master)

            cond = self._settings.renew_index
            cond = cond or not self.__node_yearbox.hasYearboxFile(self._settings.dir_data_path)

            if cond:
                self.__node_yearbox.run()
                self.__node_yearbox.save(self._settings.dir_data_path)
            else:
                self.__node_yearbox.load(self._settings.dir_data_path)

    def __p02_processsClustersInfo(self, step):
        if self._isInTestStep(step):
            self.__node_cluster_info = FBTAClusterInfo(self._settings, self._configs, self.__node_yearbox)
            self.__node_cluster_info.run()

    def __p03_processDownloader(self, step):
        if self._isInTestStep(step):
            # Step01 Download Activity
            dl = FBTAHistoryDownloadManager(self.__node_master,
                                            self.__node_cluster_info.clusters)
            dl.main()

    def __p04_processDatabaseAsCard(self, step):
        if self._isInTestStep(step):
            analysis = FBTAActivityToCardsNew(self._settings, self._configs)
            analysis.main()

    def __p05_processCardAsPost(self, step):
        if self._isInTestStep(step):
            order = FBTACardsDownloadManager(self.__node_master)
            order.main()

    def __processAlbumParse(self, step):
        if self._isInTestStep(step):
            import fbta_060_00_album_parse
            fbta_060_00_album_parse.main(self.__node_master.settings.db_name)

    def __p09_processSingleAlbum(self, step):
        if self._isInTestStep(step):
            from fbta_090_album_single_surway_manager import FBTA090AlbumSingSurvey
            album_surway = FBTA090AlbumSingSurvey(self.__node_master)
            album_surway.main()

    def __p07_crate_album(self, step):
        if self._isInTestStep(step):
            import fbta_070_00_create_no_duplicate_album
            fbta_070_00_create_no_duplicate_album.main(self.__node_master.settings.db_name)

    def __p08_crate_photo(self, step):
        if self._isInTestStep(step):
            import fbta_080_00_create_no_duplicate_photo
            fbta_080_00_create_no_duplicate_photo.main(self.__node_master.settings.db_name)

    def __p10_crate_photo_from_album(self, step):
        if self._isInTestStep(step):
            import fbta_100_00_create_photo_from_album
            fbta_100_00_create_photo_from_album.main(self.__node_master.settings.db_name)

    def __p11_processEazyPhotoDownload(self, step):
        if self._isInTestStep(step):
            from fbta_110_00_photos_download_manager import FBTA11000PhotosDownloadManager
            dl = FBTA11000PhotosDownloadManager(self.__node_master)
            dl.main()
