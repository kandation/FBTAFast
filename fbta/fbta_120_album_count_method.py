import datetime
import json
import random
import re
import time
from typing import List, Optional

from fbta_browser_worker_new import FBTAWorkerBrowserS
from fbta_global_database_manager import FBTADBManager
from fbta_node_master import FBTANodeMaster
from urllib.parse import parse_qs

from fbta_node_worker import FBTANodeWorker
from fbta_log import log

from parsel import Selector
from urllib.parse import urljoin
import html


class FBTAAlbumCountMethod:
    NONE = None

    def __init__(self, browser: FBTAWorkerBrowserS):
        self.browser = browser

