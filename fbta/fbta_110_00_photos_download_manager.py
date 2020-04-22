from fbta_110_00_photos_download_worker import FBTA11000PhotosDownloadWorker

from fbta_main_manager import FBTAMainManager
from fbta_node_master import FBTANodeMaster


class FBTA11000PhotosDownloadManager(FBTAMainManager):
    def __init__(self, node_master: FBTANodeMaster):
        self.__node_master = node_master
        print('Init Timeline History')

        __db_list = ['99_photos_tank',
                     '99_photos_tank']
        FBTAMainManager.__init__(self, self.__node_master, __db_list, FBTA11000PhotosDownloadWorker)

    def main(self):
        self._main()

    def _set_db_custom_find(self):
        key = {'user-info.ignore': {'$exists': False}}
        self.db.set_custom_find(key)
