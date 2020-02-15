from fbta_02_clusters import FBTAClusterInfo
from fbta_08_album_count_worker import FBTAAlbumCountWorker
from fbta_global_database_manager import FBTADBManager
from fbta_03_history_download_method import FBTAHistoryDownloaderMethod
from fbta_03_history_download_worker import FBTAHistoryDownloadWorker
from fbta_main_manager import FBTAMainManager
from fbta_node_master import FBTANodeMaster


class FBTAAlbumCountManager(FBTAMainManager):
    def __init__(self, node_master: FBTANodeMaster):
        self.__node_master = node_master
        print('Init Timeline History')

        __db_list = [self.__node_master.configs.db_collection_03_post_name,
                     self.__node_master.configs.db_collection_05_album_count_name]
        FBTAMainManager.__init__(self, self.__node_master, __db_list, FBTAAlbumCountWorker)

    def main(self):
        self._main()

    def _set_db_custom_find(self):
        if self.settings.use_resume:
            key = {'album-next-downloaded': {'$exists': False}, 'dataft.dataft-type': {'$exists': True}}
        else:
            key = {'dataft.dataft-type': {'$exists': True}}
        self.db.set_custom_find(key)
        self.db.get_find_docs_count()
        print(f"+++++++++++++++++++ DO THIS {self.db.get_find_docs_count()}")

    def stop_main_condition(self) -> bool:
        pass
