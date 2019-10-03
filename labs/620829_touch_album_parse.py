import html
import json
import re
from urllib.parse import unquote
import bs4

with open('./labs/test.txt', mode='r') as fo:
    text = fo.read()

text = text.replace('false', 'False')
text = text.replace('true', 'True')

py = eval(text)

exit()
text = text.replace('class="acw"', "class='acw'")
# text = text.replace('\\', '')
# text = html.unescape(text)
# py = eval(text)
REG = '(?:"html":")(.*?)(?:div>")'
kk = re.findall(REG, text)
# print(text)
text = text.replace(kk[0],'+222+')
# text = text.replace('require("ServerJS")',"require('ServerJS')")
sss = str(html.unescape(kk[0]+'div>'))
sss=sss.replace('\\u003C','<')
sss=sss.replace('\\"','"')
sss=sss.replace('\\/','/')
aaa = bs4.BeautifulSoup(sss, 'lxml')
# sss = bs4.BeautifulSoup(, 'lxml')
# sss = bs4.BeautifulSoup(, 'lxml')
aaa = aaa.find_all('a')
for aa in aaa:
    print('https://touch.facebook.com'+unquote(aa['href'].encode().decode('unicode-escape')))
# print(text)
# py = eval(text)