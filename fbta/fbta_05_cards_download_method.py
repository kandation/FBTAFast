import datetime
import random
import time

from fbta_global_database_manager import FBTADBManager
from fbta_node_master import FBTANodeMaster
from urllib.parse import parse_qs

from fbta_node_worker import FBTANodeWorker
from fbta_log import log


class FBTACardsDownloaderMethod:
    NONE = None
    """
    HistoryDownloadMethod Work like 'activity_download.py'
    but now it include in 'fbta_03_history_download_manager.py'
    """

    def __init__(self, node_master: FBTANodeMaster, worker_browser: FBTANodeWorker, db: FBTADBManager):
        self.__worker_driver = worker_browser.browser.driver
        self.db = db
        self.node_master = node_master
        self.__settings = self.node_master.settings
        self.__configs = self.node_master.configs

