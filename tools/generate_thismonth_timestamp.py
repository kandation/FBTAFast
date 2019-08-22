import json
from datetime import datetime
from pprint import pprint

"""
Generate Yearbox Lastest Timestamp for FBTAV1.03
"""

if __name__ == '__main__':
    pass

def getLasttimeInFile():
    with open('yearbox.json', mode='r', encoding='utf8') as fo:
        data:dict = json.loads(fo.read())
    mx = max([max([x.get('date') for x in d.get('month')]) for d in data.values()])
    return mx
