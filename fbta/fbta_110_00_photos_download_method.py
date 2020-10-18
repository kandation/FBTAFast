import datetime
import json
import random
import re
import time
from typing import List, Optional

from fbta.fbta_browser_worker_new import FBTAWorkerBrowserS
from fbta.fbta_log import log

from parsel import Selector
from urllib.parse import urljoin
import html


class FBTA11000PhotosDownloadMethod:
    NONE = None

    def __init__(self, browser: FBTAWorkerBrowserS):
        self.browser = browser

    def get_hops(self, url):
        redirect_re = re.compile('<meta[^>]*?url=(.*?)["\']', re.IGNORECASE)
        hops = []
        while url:
            if url in hops:
                url = None
            else:
                hops.insert(0, url)
                response = self.browser.goto(url, True)
                if response.url != url:
                    hops.insert(0, response.url)
                # check for redirect meta tag
                if response.encoding is not None:
                    match = redirect_re.search(response.text)
                    if match:
                        ref_url = match.groups()[0].strip()
                        if 'http' not in ref_url[:10]:
                            print('-----[Photo-Method] http not in ref url', ref_url)

                            url = urljoin(url, html.unescape(ref_url))
                        else:
                            url = html.unescape(ref_url)

                    else:
                        url = None
                else:
                    url = None
        return hops
