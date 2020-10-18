from fbta.fbta_02_clusters import FBTAClusterInfo
from fbta.fbta_global_database_manager import FBTADBManager
from fbta.fbta_03_history_download_method import FBTAHistoryDownloaderMethod
from fbta.fbta_03_history_download_worker import FBTAHistoryDownloadWorker
from fbta.fbta_main_manager import FBTAMainManager
from fbta.fbta_node_master import FBTANodeMaster


class FBTAHistoryDownloadManager(FBTAMainManager):
    def __init__(self, node_master: FBTANodeMaster, cluster_info: FBTAClusterInfo):
        self.__node_master = node_master
        print('Init Timeline History')

        __db_list = [self.__node_master.configs.db_collection_00_yearbox_name,
                     self.__node_master.configs.db_collection_01_page_name]
        FBTAMainManager.__init__(self, self.__node_master, __db_list, FBTAHistoryDownloadWorker)

    def main(self):
        self._main()