import time
from pprint import pprint

from fbta.fbta_04_activity_to_card import FBTAActivityToCardsNew
from fbta.fbta_05_cards_download_manager import FBTACardsDownloadManager
from fbta.fbta_02_clusters import FBTAClusterInfo
from fbta.fbta_06_photos_download_manager import FBTAPhotosDownloadManager
from fbta.fbta_07_dataft import FBTADataft
# from fbta.fbta_120_album_count_manager import FBTAAlbumCountManager
from fbta.fbta_configs import FBTAConfigs
from fbta.fbta_03_history_download_manager import FBTAHistoryDownloadManager
from fbta_mkdir import FBTAMkdir
from fbta_node_master import FBTANodeMaster
from fbta_sequence_func import FBTASequenceFunction
from fbta_settings import FBTASettings
from fbta_01_yearbox import FBTAYearBox


class FBTASequence(FBTASequenceFunction):
    def __init__(self, setting: FBTASettings, configs: FBTAConfigs):
        FBTASequenceFunction.__init__(self, setting, configs)

        self.__node_master: FBTANodeMaster = FBTANodeMaster.NONE

        self.__node_yearbox = None
        self.__node_cluster_info: FBTAClusterInfo = None

    def start(self):
        self._warnningTimeOptimize()
        self.__px0_initDirectory()

        self.__p00_generateMasterNode(0)
        self._showFinishedProcessEndNotify(0)

        self.__p01_processYearBox(1)
        self._showFinishedProcessEndNotify(1)

        self.__p02_processsClustersInfo(2)
        self._showFinishedProcessEndNotify(2)

        self.__p03_processDownloader(3)
        self._showFinishedProcessEndNotify(3)

        self.__p04_processDatabaseAsCard(4)
        self._showFinishedProcessEndNotify(4)

        self.__p05_processCardAsPost(5)
        self._showFinishedProcessEndNotify(5)

        self.__processDonloadPhotos(6)
        self._showFinishedProcessEndNotify(6)

        self.__processDataft(7)
        self._showFinishedProcessEndNotify(7)

        self.__p08_processAlbumCount(8)
        self._showFinishedProcessEndNotify(8)
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

    def __processDonloadPhotos(self, step):
        if self._isInTestStep(step):
            photos = FBTAPhotosDownloadManager(self.__node_master)
            photos.main()

    def __p08_processAlbumCount(self, step):
        if self._isInTestStep(step):
            album_count = FBTAAlbumCountManager(self.__node_master)
            album_count.main()

    def __processDataft(self, step):
        if self._isInTestStep(step):
            dataft = FBTADataft(self.__node_master)
            dataft.main()