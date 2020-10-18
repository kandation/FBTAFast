from fbta.fbta_05_cards_download_worker import FBTACardsDownloadWorker
from fbta.fbta_main_manager import FBTAMainManager
from fbta.fbta_node_master import FBTANodeMaster


class FBTACardsDownloadManager(FBTAMainManager):
    def __init__(self, node_master: FBTANodeMaster, step_find_album_count=False):
        self.__node_master = node_master
        print('Init Cards History')
        self.__chrome_header = step_find_album_count

        if not step_find_album_count:
            __db_list = [self.__node_master.configs.db_collection_02_card_name,
                         self.__node_master.configs.db_collection_03_post_name]
        else:
            __db_list = ['98_album_no_duplicate',
                         '98_album_no_duplicate']
        FBTAMainManager.__init__(self, self.__node_master, __db_list, FBTACardsDownloadWorker,
                                 chrome_header=step_find_album_count)

    def _set_db_custom_find(self):
        if self.__chrome_header:
            key = {'photo-cluster.0.is-more': {'$ne': ''}}
            self.db.set_custom_find(key, recheck_key=False)

    def main(self):
        self.clear_db_downloaded_key()
        self._main()

    def stop_main_condition(self) -> bool:
        pass
