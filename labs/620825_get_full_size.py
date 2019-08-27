from pprint import pprint

import requests
from parsel import Selector

re = requests.get('https://m.facebook.com/2416468638412634', allow_redirects=True)
# print(str(re.text))

bs = Selector(re.text)
# View Full Size
k = bs.xpath("//a[contains(.,'ดูภาพขนาดเต็ม')]").attrib.get('href')
print(k)