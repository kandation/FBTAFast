from time import time, sleep


class FBTATimer:
    def __init__(self):
        self.__event = {}

    def add(self, name):
        self.__event[name] = time()

    def is_time(self, event, sec):
        return time() - self.__event.get(event) >= sec

    def update(self, event):
        self.__event[event] = time()

    @property
    def event(self):
        return self.__event
