import requests
import json
import pprint
import shutil
import os
import urllib.request

import time, random
class FacebookAlbumDownload:
    def __init__(self, config):
        self.config = config
        self.config['main-url'] = 'https://graph.facebook.com/v3.2/'

    def check_config(self):
        if 'token' not in self.config:
            print('Please Insert token or renew @ https://developers.facebook.com/tools/explorer/')
            exit()

    def __connect(self, command):
        while True:
            http_header = {"Authorization": "OAuth " + self.config['token']}
            grahp_url = self.config['main-url'] + str(command)
            rand_connect = random.randint(1,7)
            time.sleep(rand_connect)
            r = requests.get(grahp_url, headers=http_header)
            res = json.loads(r.text, encoding='utf-8')
            error = self.error_handlling(res)
            if error:
                if error['code'] == 'wait-limit':
                    print('Facebook Limit Your Links wait 120 sec to Next process')
                    time.sleep(120)
            else:
                return res
    def error_handlling(self, res):
        """{'error': {'message': '(#4) Application request limit reached', 'type': 'OAuthException', 'is_transient': True, 'code': 4, 'fbtrace_id': 'Ba23crLN+SS'}}"""
        if 'error' in res.keys():
            code = res['error']['code']
            if code  == 4:
                return {'error': True, 'code': 'wait-limit'}
            if code == 190:
                print('Parameter Error or old token visit@ https://developers.facebook.com/tools/explorer/')
                exit()
            if code >= 0:
                print(res)
                print('unkonw error')
                exit()
        else:
            return False

    def __cmd_album(self, aid):
        field = '?fields=count,link,type,photos.limit(999999){images,comments.limit(999){comment_count,permalink_url},picture,name},description,photo_count,video_count'
        return str(aid) + field

    def get_album_js(self, aid):
        return self.__connect(self.__cmd_album(aid))

    def get_all_photoes(self, aid):
        couter = 0
        data = []
        fo = open(str(aid), mode='w', encoding='utf8')
        f = self.get_album_js(aid)

        for p in f['photos']['data']:
            # print(p['images'][0])
            data.append(p['images'][0])
            fo.write(str(p['images'][0]))
            couter += 1

        try:
            next = f['photos']['paging']['next']
            # print(f['photos']['paging'])
            next_none = str(next).replace(self.config['main-url'], '')
            print(next_none)
            print('Now Couter', couter)

            while True:
                f = self.__connect(next_none)

                # print(f)
                for p in f['data']:
                    # print(p['images'][0])
                    data.append(p['images'][0])
                    fo.write(p['images'][0])
                    couter += 1
                print('Now Couter', couter)

                if 'next' in f['paging'].keys():
                    next = f['paging']['next']
                    # print(f['paging'])
                    next_none = str(next).replace(self.config['main-url'], '')
                    print(next_none)
                else:
                    break
        except:
            pass

        fo.close()

        import json
        with open(str(aid), mode='w', encoding='utf8') as fo:
            fo.write(str(json.dumps(data, ensure_ascii=False)))

    def getNameFormLink(self, url):
        import re

        re1 = '.*?'  # Non-greedy match on filler
        re2 = '\\d+'  # Uninteresting: int
        re3 = '.*?'  # Non-greedy match on filler
        re4 = '\\d+'  # Uninteresting: int
        re5 = '.*?'  # Non-greedy match on filler
        re6 = '\\d+'  # Uninteresting: int
        re7 = '.*?'  # Non-greedy match on filler
        re8 = '\\d+'  # Uninteresting: int
        re9 = '.*?'  # Non-greedy match on filler
        re10 = '(\\d+)'  # Integer Number 1

        rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8 + re9 + re10, re.IGNORECASE | re.DOTALL)
        m = rg.search(url)
        if m:
            int1 = m.group(1)
            return int1

    def getFileOnInternet(self,name, url):
        # Stream download for large files
        response = requests.get(url, stream=True)
        ty = response.headers['Content-Type'].split('/', 1)
        rt = {'jpeg': 'jpg', 'png': 'png'}
        ty = rt[ty[1]]
        print("downloading: " + name + '.' + ty)
        with open('./aa/'+str(name) + '.' + ty, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

    def largeFile(self,aid):
        with open(str(aid), mode='r', encoding='utf8') as fo:
            data = json.loads(fo.read(), encoding='utf8')
        for i,u in enumerate(data):
            link = u['source']

            name = self.getNameFormLink(link)
            prefix_n = len(str(len(data)))
            print(len(data))
            prefix = str(i).zfill(prefix_n)

            self.getFileOnInternet(prefix+'_'+name,link)
            print(name)




config = {
    'token': 'EAAByuLcXwQgBALUzjBMQMhsamIlXz8vxiOFE40Ru7TkmfZAZAqQLuYeKZAecLcfSxH9fNKkVkoZANUOyyZAW6Dx7aZCJOBZCShYB5kWsLZC05q9KvjatY1BC3PlIetYpZCxlTMicagZBOwvb2KCci4YWQKsBuGBiIsg9KUQpVMnZBFASKJ7rJYJjxylc2A7GlWNmOa3eiZB442wIqAZDZD'
}
fb = FacebookAlbumDownload(config)
f = fb.get_album_js('475035875862919')
# print(f.keys())
print(f['count'])
fb.get_all_photoes(475035875862919)
fb.largeFile(475035875862919)
# fb.largeFile(145323788830814)
#
