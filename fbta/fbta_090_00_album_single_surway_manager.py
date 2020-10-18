from fbta.fbta_090_00_album_single_surway_worker import FBTA090AlbumSingSurveyWorker

from fbta.fbta_main_manager import FBTAMainManager
from fbta.fbta_node_master import FBTANodeMaster


class FBTA090AlbumSingSurvey(FBTAMainManager):
    def __init__(self, node_master: FBTANodeMaster):
        self.__node_master = node_master
        print('Init Timeline History')

        __db_list = ['98_album_no_duplicate',
                     '98_album_no_duplicate']
        FBTAMainManager.__init__(self, self.__node_master, __db_list, FBTA090AlbumSingSurveyWorker)

    def main(self):
        self._main()
    #
    # def _set_db_custom_find(self):
    #     self.db.get_find_docs_count()
    #     print(f"+++++++++++++++++++ DO THIS {self.db.get_find_docs_count()}")

