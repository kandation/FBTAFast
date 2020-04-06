from bs4 import BeautifulSoup
with open('Labs/620902_albumdl/test_case/6209021742_timeline.js', mode='r') as fo:
    data = fo.read()

js_obj =data

import demjson

# from
# js_obj = '{x:1, y:2, z:3}'

# to
py_obj = demjson.decode(js_obj)
k = py_obj['domops'][0][3]['__html']
print(k)
bs =BeautifulSoup(k,'lxml')
print(bs.prettify())