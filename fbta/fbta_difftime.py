import time

from datetime import datetime


class FBTADifftime:
    def __init__(self):
        pass

    @staticmethod
    def printTimeDiff(starttime):
        iTime = time.time() - starttime
        withSecStr = '{} Minites {} Sec ({})'.format(int(iTime // 60), iTime - ((iTime // 60) * 60), iTime)
        sTime = str(iTime) + ' Sec' if iTime < 60 else withSecStr
        return sTime

    @classmethod
    def timestamp2date(cls, __time_startNow):
        return datetime.fromtimestamp(__time_startNow)
