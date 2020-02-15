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


class FBTAPhotosDownloadMethod:
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

    def find_type_of_post(self, doc):
        bs = Selector(doc.get('source', ''))
        dataft_list: List[Optional[Selector]] = bs.css("div[data-ft]")
        if len(dataft_list) == 0:
            log('Error DOCS_NONE_FT', 'https://m.facebook.com' + doc['url'])
            # if 'story' in doc['url']:
            #     print(doc['source'])
        else:
            max_indexx = [len(x.attrib['data-ft']) for x in dataft_list]
            max_index = max_indexx.index(max(max_indexx))
            return self.dataparse(dataft_list[max_index].attrib['data-ft'])
        return '-1'

    def dataparse(self, ft):
        js = json.loads(ft, encoding='utf8')
        k = js.get('attached_story_attachment_style')
        ppps = ['photo', 'album', 'share', 'video_inline', 'cover_photo', 'animated_image_share', 'profile_media',
                'new_album', 'page_insights', 'animated_image_video', 'video_direct_response', 'commerce_product_item',
                'event', 'video_share_highlighted', 'avatar', 'native_templates', 'note']
        if k in ppps and k is not None:
            if k == 'photo':
                # print('https://m.facebook.com/'+js['tl_objid'])
                return js['photo_id']
                # print(js)
            if k == 'cover_photo':
                if js.get('photo_id'):
                    return js['photo_id']

        return '-1'
