from typing import List, Optional

import pymongo
from pymongo import MongoClient

from fbta_log import log


class FBTADBManager:
    """
    :parameter:
    - db_name: mongo database name
    - collection_list: [current_collection, next_collection]
    """

    def __init__(self, dbname: str, collection_list: list = None, stat_coll=None):
        self.current_num = 0
        self.db_skipter = 0
        self.clusters_num = 0
        self.__collection_list = collection_list

        self.__db_cardnum = 0

        self.db_index = 0
        self.db_process_skipter = 0

        self.__docs_list_waiting: List[Optional[pymongo.cursor.Cursor]] = []

        self.__db_cards_temp = List[Optional[pymongo.cursor.Cursor]]

        if self.__collection_list:
            current_coll = collection_list[0] if collection_list[0] else 'error_collection'
            next_coll = collection_list[1] if collection_list[1] else 'error_collection'

            self.__client: MongoClient = MongoClient()
            self.__db: pymongo.mongo_client.database.Database = self.__client.get_database(dbname)

            self.__currentCollection: pymongo.collection = self.__db.get_collection(current_coll)
            self.__nextCollection: pymongo.collection = self.__db.get_collection(next_coll)

            self.__prop_currntCollection_name: str = current_coll
            self.__prop_nextCollection_name: str = next_coll

            self.__data_list: List[Optional[pymongo.cursor.Cursor]] = []

            self.current_num = self.getCurrentCollection_num()

    def get_loop_time(self):
        return 2 if int(0.05 * self.current_num) <= 0 else int(0.05 * self.current_num) + 1

    @property
    def docs_num(self):
        return self.__db_cardnum

    @docs_num.setter
    def docs_num(self, val):
        self.__db_cardnum = val

    def getCurrentCollection_num(self):
        return self.__currentCollection.count()

    def checkCurrentIsNotEmpty(self):
        if self.getCurrentCollection_num() < 0:
            raise Exception(self.__prop_currntCollection_name, 'Database is Empty')

    def getCurrentDocsByLimit(self, start, length) -> pymongo.cursor.Cursor:
        log(f':DBMange: \t■■■■■■■ DB Load with startPage=[{start}] to [{start + length - 1}] with[{length}]')
        return self.__currentCollection.find(no_cursor_timeout=True).skip(start).limit(length)

    def current_insert_one(self, data: dict):
        return self.__currentCollection.insert_one(data)

    def current_insert_many(self, data: list):
        return self.__currentCollection.insert_many(data)

    def current_drop(self):
        return self.__currentCollection.drop()

    def next_collection_insert_one(self, data: dict):
        return self.__nextCollection.insert_one(data)

    @property
    def is_db_can_run(self):
        return bool(self.__collection_list)

    @property
    def docs_list(self) -> List[Optional[pymongo.cursor.Cursor]]:
        return self.__data_list

    @property
    def docs_list_waiting(self) -> List[Optional[dict]]:
        return self.__docs_list_waiting

    @property
    def cards_temp(self) -> List[Optional[pymongo.cursor.Cursor]]:
        return self.__db_cards_temp

    @cards_temp.setter
    def cards_temp(self, val):
        self.__db_cards_temp = val

    def cal_start_index(self):
        return self.db_index * self.db_skipter
