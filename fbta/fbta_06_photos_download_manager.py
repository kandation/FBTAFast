from fbta.fbta_02_clusters import FBTAClusterInfo
from fbta.fbta_06_photos_download_worker import FBTAPhotosDownloadWorker
from fbta.fbta_global_database_manager import FBTADBManager
from fbta.fbta_03_history_download_method import FBTAHistoryDownloaderMethod
from fbta.fbta_03_history_download_worker import FBTAHistoryDownloadWorker
from fbta.fbta_main_manager import FBTAMainManager
from fbta.fbta_node_master import FBTANodeMaster


class FBTAPhotosDownloadManager(FBTAMainManager):
    def __init__(self, node_master: FBTANodeMaster):
        self.__node_master = node_master
        print('Init Timeline History')

        __db_list = [self.__node_master.configs.db_collection_03_post_name,
                     self.__node_master.configs.db_collection_04_photo_name]
        FBTAMainManager.__init__(self, self.__node_master, __db_list, FBTAPhotosDownloadWorker)

    def main(self):
        self._main()

    def stop_main_condition(self) -> bool:
        pass
