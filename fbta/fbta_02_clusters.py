from pprint import pprint

from fbta.fbta_configs import FBTAConfigs
from fbta.fbta_global_database_manager import FBTADBManager
from fbta.fbta_settings import FBTASettings
from datetime import datetime

from fbta.fbta_01_yearbox import FBTAYearBox
from fbta.fbta_log import log


class FBTAClusterInfo:
    def __init__(self, settings: FBTASettings, configs: FBTAConfigs, yearbox: FBTAYearBox):
        self.__settingsClass = settings
        self.__configs = configs
        self.__yearbox = yearbox

        self.__clusterNum = 1
        self.__updateSettings()

        self.__clusters = None

        self.__clusterLimit = 15

    def __updateSettings(self):
        __clusterNum = self.__settingsClass.cluster_num
        self.__clusterNum = __clusterNum if __clusterNum > 0 else 1

        self.__clusterLimit = self.__settingsClass.cluster_limit
        self.__clusterNum = self.__calculateClusterslimit(__clusterNum)

    def setClusterNum(self, num):
        self.__clusterNum = num

    def getClusters(self):
        if self.__clusters is None:
            self.run()
        return self.__clusters

    def __getDateStart(self):
        dateStart = self.__settingsClass.date_process
        dateStart = self.__reduceDateStart(dateStart) if dateStart is not None else datetime(1900, 1, 1)
        return dateStart

    def __reduceDateStart(self, dd) -> datetime:
        tempDate = [1990, 1, 1]
        for i in range(len(dd) - 1):
            tempDate[i] = dd[i]
        return datetime(tempDate[0], tempDate[1], tempDate[2])

    def __reduceListAllMonth(self, reversed=False) -> list:
        newMonthSequnce = []
        for items in self.__yearbox.getYearbox().values():
            for month in items['month']:
                month['_id'] = str(int(month['date']))
                dateStart = self.__getDateStart()
                dateNow = datetime.fromtimestamp(month['date'])
                if dateNow >= dateStart:
                    newMonthSequnce.append(month)


        from operator import itemgetter
        newMonthSequnce.sort(key=itemgetter('date'), reverse=reversed)

        return newMonthSequnce

    def __calculateClusterslimit(self, __clusterNum):
        return __clusterNum if __clusterNum <= self.__clusterLimit else 15

    def __calculateClusterMonthSeq(self, monthSeq):
        cluster = len(monthSeq) if len(monthSeq) <= self.__clusterNum else self.__clusterNum
        self.__clusterNum = cluster
        return cluster

    def __getCluserterInfo(self, monthSequence: list) -> dict:
        clusterNum = self.__clusterNum

        clusters = {
            'num': clusterNum,
            'data': monthSequence
        }

        notifyClusterInfoText = 'ClusterInfo: Generate Clusters OK \n\t>> ClusterNum = '
        log(notifyClusterInfoText, clusterNum)

        return clusters

    def run(self) -> dict:
        monthSeq = self.__reduceListAllMonth(reversed=False)  # False when lasted month is End
        self.__calculateClusterMonthSeq(monthSeq)
        self.__clusters = self.__getCluserterInfo(monthSeq)

        self.__clusters_to_database()

        return self.__clusters

    def __clusters_to_database(self):
        db_collections = [self.__configs.db_collection_00_yearbox_name, None]
        db = FBTADBManager(self.__settingsClass.db_name, db_collections, self.__configs.db_collection_stat)
        db.current_insert_many(self.clusters['data'])


    @property
    def clusters(self):
        return self.__clusters
