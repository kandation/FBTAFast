from typing import List, Optional

import pymongo
from pymongo import MongoClient

from fbta_difftime import FBTADifftime
from fbta_log import log


class FBTADBManager:
    """
    :parameter:
    - db_name: mongo database name
    - collection_list: [current_collection, next_collection]
    """

    def __init__(self, dbname: str, collection_list: list = None, stat_coll=None):
        self.collect_current_total_docs_find = 0
        self.db_skipter = 0
        self.clusters_num = 0
        self.__collection_list = collection_list

        self.__db_cardnum = 0

        self.db_index = 0
        self.db_process_skipter = 0

        self.__docs_list_waiting: List[Optional[pymongo.cursor.Cursor]] = []

        self.__db_cards_temp = List[Optional[pymongo.cursor.Cursor]]

        self.__find_condition = {}

        self.total_docs_first_find = 0

        if self.__collection_list:
            current_coll = collection_list[0] if collection_list[0] else 'error_collection'
            next_coll = collection_list[1] if collection_list[1] else 'error_collection'

            self.__client: MongoClient = MongoClient()
            self.__db: pymongo.mongo_client.database.Database = self.__client.get_database(dbname)

            self.__current_collection: pymongo.collection = self.__db.get_collection(current_coll)
            self.__collection_next: pymongo.collection = self.__db.get_collection(next_coll)
            if stat_coll:
                self.__collection_stat: pymongo.collection = self.__db.get_collection(stat_coll)

            self.__prop_current_collection_name: str = current_coll
            self.__prop_next_collection_name: str = next_coll

            self.__data_list: List[Optional[pymongo.cursor.Cursor]] = []

            self.__current_cursor_new = None

            self.collect_current_total_docs_find = -1

    def get_loop_time(self):
        return 2 if int(0.05 * self.collect_current_total_docs_find) <= 0 else int(
            0.05 * self.collect_current_total_docs_find) + 1

    def get_db_name(self) -> str:
        return self.__db.name

    @property
    def docs_num(self):
        return self.__db_cardnum

    @docs_num.setter
    def docs_num(self, val):
        self.__db_cardnum = val

    def getCurrentCollection_num(self):
        return self.__current_collection.count_documents(self.get_find_condition())

    def checkCurrentIsNotEmpty(self):
        if self.getCurrentCollection_num() < 0:
            raise Exception(self.__prop_current_collection_name, 'Database is Empty')

    def get_find_docs_count(self) -> int:
        self.collect_current_total_docs_find = self.__current_collection.count_documents(self.__find_condition)
        return self.collect_current_total_docs_find

    def get_current_docs_by_limit(self, start, length) -> pymongo.cursor.Cursor:
        log(f':DBMange: \t■■■■■■■ DB Load with startPage=[{start}] to [{start + length - 1}] with[{length}]')
        return self.__current_collection.find(self.__find_condition, no_cursor_timeout=True).skip(start).limit(length)

    def set_custom_find(self, cond: dict, recheck_key=True):
        self.__is_use_custom_find = True
        if recheck_key:
            cond['downloaded-recheck'] = {'$exists': False}
            self.__find_condition = cond
        else:
            self.__find_condition = cond

    def get_current_docs(self) -> pymongo.cursor.Cursor:
        log(f':DBMange: \t■■■■■■■ DB Load Full')
        return self.__current_collection.find(self.__find_condition, no_cursor_timeout=True)

    def current_insert_one(self, data: dict):
        return self.__current_collection.insert_one(data)

    def current_insert_many(self, data: list):
        return self.__current_collection.insert_many(data)

    def current_drop(self):
        return self.__current_collection.drop()

    def next_collection_insert_one(self, data: dict):
        return self.__collection_next.insert_one(data)

    def stat_collection_insert_one(self, data: dict):
        return self.__collection_stat.insert_one(data)

    def stat_collectioin_add_one(self, data: dict):
        find_docs = {'process-name': data.get('process-name')}
        return self.__collection_stat.update_one(find_docs, {"$set": data}, upsert=True)

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

    def __add_stat_to_db(self, name, method, start_time, end_time, stat, log_type):
        data = {
            'process-name': name,
            'process-method': method,
            'process-time-start': start_time,
            'process-time-end': end_time,
            'process-time-total-text': FBTADifftime.printTimeDiff(start_time),
            'log-type': log_type,
            'stat-data': stat,
        }

        self.stat_collectioin_add_one(data)

    def add_stat_to_db(self, name, method, start_time, end_time, stat):
        self.__add_stat_to_db(name, method, start_time, end_time, stat, 'Summery')

    def add_stat_to_db_auto(self, name, method, start_time, end_time, stat):
        self.__add_stat_to_db(name, method, start_time, end_time, stat, 'Auto-save')

    def current_get_name(self) -> str:
        return self.__current_collection.name

    def next_get_name(self) -> str:
        return self.__collection_next.name

    def raw_collection_next(self) -> pymongo.collection:
        return self.__collection_next

    def raw_collection_current(self) -> pymongo.collection:
        return self.__current_collection

    def get_find_condition(self) -> dict:
        return self.__find_condition

    @staticmethod
    def get_resume_key() -> dict:
        return {'downloaded-recheck': True}

    def update_first_find_total(self):
        self.total_docs_first_find = self.getCurrentCollection_num()

    def update_coll_current_index(self):
        self.collect_current_total_docs_find = self.getCurrentCollection_num()
