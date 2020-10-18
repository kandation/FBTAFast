"""
# COUNTING_AND_CREATE_URL_FOR_NEXT_PAGE_ALBUM
# Pre-process from LOAD_NEW_STORY_WITH_CHROME_HEADER
"""

from datetime import datetime
from time import time
import re as regex

from bson import DBRef
from pymongo import MongoClient

from fbta.fbta_log import log


class FBTA120CountingAlbumPreprocess():
    def __init__(self):
        """ Find the number of images in the album """
        pass

    def splitter_url(self, url, counter, start_img_num):
        """ แบ่ง URL จากรูปภาพเริ่มต้น"""
        url_list = []
        counter += start_img_num

        num_rem = counter % 12
        num_url = (counter // 12) if num_rem <= 0 else (counter // 12) + 1

        for c in range(1, num_url):
            load_url = f'{url}&s={12 * c}&refid=56'
            is_end = c == num_url - 1
            d = {
                'url-id': c,
                'load-url': load_url,
                'is-end': is_end
            }
            url_list.append(d)
        return url_list

    def main(self, db_name):
        PATT_ALBUM_COUNTER_NUMBER = '(?<=[\>])(\+[0-9,]+)(?=[\<])'

        client = MongoClient()
        db = client.get_database(db_name)
        collection = db.get_collection('98_album_no_duplicate')
        collection_new = db.get_collection('aa_album_url')

        key = {'photo-cluster.0.is-more': {'$ne': ''}}
        docs_post = collection.find(key)

        time_all_start = time()

        log(f':ALBUM_COUNTER: Docs in collection = {collection.count_documents(key)}')
        import copy
        for doc in docs_post:
            album_counter = doc.get('album-count')

            data = {
                'img-count': -1,
                'img-count-start': 0,
                'split-url': [],
            }

            # Recheck Tag again (Why ???)
            if album_counter:
                # Get page-source from LOAD_PAGE_WITH_CHROME_HEADER step
                source = album_counter.get('album-count-source')
                is_ignore = doc.get('user-info').get('ignore', False)

                oid = doc.get('_id')
                first_ref = doc.get('ref')[0]

                str_more_img = ''.join(regex.findall(PATT_ALBUM_COUNTER_NUMBER, source))
                str_more_img = str_more_img.replace('+', '').replace(',', '').strip()

                # Call Ref_ALBUM cause need START_IMG_NUM in story
                ref_album_duplicate = first_ref
                ref_album_dup_obj = db.dereference(ref_album_duplicate)

                # get START_IMG_NUM from exist key (in Collection)
                old_img_tag = ref_album_dup_obj['description']['album']['data-album']['album-cluster']['img']
                num_old_img = sum([len(old_img_tag[key_cx]) for key_cx in old_img_tag])
                data['img-count-start'] = num_old_img

                if str_more_img:
                    urlx = doc.get('photo-cluster').get('url')
                    ls = self.splitter_url(urlx, int(str_more_img), num_old_img)

                    data['split-url'] = ls
                    data['img-count'] = int(str_more_img)

                    ref_for_more_album = DBRef(collection.name, oid, db.name)

                    for lsx in ls:
                        lsx['ref'] = ref_for_more_album
                        lsx['user-ignore'] = is_ignore
                        collection_new.insert_one(lsx)

                else:
                    """
                    อาจจะเกิดจากความผิดพลาด ตอน Restart browser
                    """
                    data['error'] = {'code': 'browser-restart'}

                data = {'album-count-num': data}
                print(data)
                collection.update({'_id': oid}, {'$set': data})

        print('Finished', time() - time_all_start)


if __name__ == '__main__':
    nno = FBTA120CountingAlbumPreprocess()
    nno.main('fbta_20200422_0239')
