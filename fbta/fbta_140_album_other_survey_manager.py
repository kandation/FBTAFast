from fbta.fbta_090_00_album_single_surway_worker import FBTA090AlbumSingSurveyWorker
from fbta.fbta_140_album_other_survey_worker import FBTA140AlbumOtherSurveyWorker

from fbta.fbta_main_manager import FBTAMainManager
from fbta.fbta_node_master import FBTANodeMaster


class FBTA140AlbumOtherSurvey(FBTAMainManager):
    def __init__(self, node_master: FBTANodeMaster):
        self.__node_master = node_master
        print('Init Timeline History')

        __db_list = ['aa_album_url',
                     'aa_album_url']
        FBTAMainManager.__init__(self, self.__node_master, __db_list, FBTA140AlbumOtherSurveyWorker)

    def main(self):
        self._main()

    def _set_db_custom_find(self):
        key = {'user-ignore': False}
        self.db.set_custom_find(key)


    def stop_main_condition(self) -> bool:
        pass
