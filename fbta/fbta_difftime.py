import time

from datetime import datetime


class FBTADifftime:
    def __init__(self):
        pass

    @staticmethod
    def printTimeDiff(starttime):
        res = time.time() - starttime
        return FBTADifftime.time2string(res)

    @staticmethod
    def time2string(sec):
        str_time = ''
        t_hour = int(sec // 3600)
        t_min = int((sec - t_hour * 3600) // 60)
        t_sec = int(int(sec) - t_hour * 3600 - t_min * 60)
        if sec > 3600:
            str_time += f'{t_hour} Hours '
        if sec > 60:
            str_time += f'{t_min} Minutes '
        str_time += f'{t_sec} Sec ({int(sec)})'
        return str_time

    @staticmethod
    def printTimeDiffWithStart(start, stop):
        res = stop - start
        return FBTADifftime.time2string(res)

    @classmethod
    def timestamp2date(cls, __time_startNow):
        return datetime.fromtimestamp(__time_startNow)
