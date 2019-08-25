from fbta_05_cards_download_worker import FBTACardsDownloadWorker
from fbta_main_manager import FBTAMainManager
from fbta_node_master import FBTANodeMaster


class FBTACardsDownloadManager(FBTAMainManager):
    def __init__(self, node_master: FBTANodeMaster):
        self.__node_master = node_master
        print('Init Cards History')

        __db_list = [self.__node_master.configs.db_collection_02_card_name,
                     self.__node_master.configs.db_collection_03_post_name]
        FBTAMainManager.__init__(self, self.__node_master, __db_list, FBTACardsDownloadWorker)

    def main(self):
        self._main()

    def stop_main_condition(self) -> bool:
        pass
