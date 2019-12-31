import json


class FBTAStatistic:
    def __init__(self):
        self.worker_couter_docs = 0
        self.worker_browser_died = 0
        self.history_couter_success = 0
        self.history_couter_fail = 0
        self.history_couter_screenshot_success = 0
        self.history_couter_screenshot_fail = 0

        self.history_time_global_start = 0

        self.custom_stat = {}

    def get_worker_stat(self, name) -> str:
        __stat = {'id': name, 'stat': self.__get_class_dict()}
        return str(json.dumps(__stat))

    def get_worker_stat_json(self, name):
        __stat = {'id': name, 'stat': self.__get_class_dict()}
        return json.dumps(__stat)

    def get_worker_stat_dict(self, name):
        __stat = {'id': name, 'stat': self.__get_class_dict()}
        return __stat

    def __get_class_dict(self):
        stat = {}
        for key in self.__dict__:
            stat[key] = self.__dict__[key]
        return stat

    def add_stat(self, key):
        if self.custom_stat.get(key):
            self.custom_stat[key] += 1
        else:
            self.custom_stat[key] = 1

    def add_stat_static(self, key, value):
        self.custom_stat[key] = value

    def json_to_stat(self, param):
        return json.loads(param)


if __name__ == '__main__':
    s = FBTAStatistic()
    print(s.get_worker_stat('ss'))
    # s.print_dic()
