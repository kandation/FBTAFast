import datetime
import os
from typing import Any


# from fbta_keyinterupt import FBTAKeyInterupt


class FBTASettings:
    _DIR_DETAIL_NEW_ALL_RUN = 'dir_detail_new_all_run'
    _DIR_DETAIL_NEW_ON_DAY = 'dir_detail_new_on_day'

    def __init__(self, username):
        self.headerless = False
        self.__dir_save_prefix = 'save_'
        self.__is_user_init_db = False
        self.__dir_path = r'./'
        self.dir_save_path = r'./save/'

        self.init_node_master_browser = True
        self.dir_data_path = './'
        self.username = username
        self.cluster_limit = 50
        self.cluster_num = 4
        self.__db_prefix = 'fbta'
        self.db_name = None
        self.renew_index = False

        self.renew_login = False

        self.date_process = None
        self.driver_path = r'.'
        self.password_key = r'./key.key'
        self.password_enc = r'./password.enc'
        self.use_nodeMaster = True
        self.use_nodeSlave = True
        self.use_nodeMaster_loadCookie = False
        self.test_step = []
        self.dir_path_detail = self.DIR_DETAIL_NEW_ON_DAY
        self.is_auto_dbname = False

        self.use_resume = False

        self.run_fast_all = False
        self.run_fast_cluster_info = False

        # self.__keykill = FBTAKeyInterupt()

        self.fast_worker = False

        self.__userinfo = {}

        self.__autoInit()

        self.__killdriveronend = True

        self.dir_cookies = r'./'
        self.dir_yearbox = r'./'

        self.__ignore_name = -1

    @property
    def run_fast_cluster_info(self):
        return self.__run_fast_cluster_info

    @run_fast_cluster_info.setter
    def run_fast_cluster_info(self, cond=False):
        self.__run_fast_cluster_info = bool(cond)

    def getProjectPath(self, path) -> str:
        return self.dir_path + '/' + path

    @property
    def kill_driver_on_end(self):
        return self.__killdriveronend

    @kill_driver_on_end.setter
    def kill_driver_on_end(self, cond: bool):
        self.__killdriveronend = bool(cond)

    # @property
    # def keykill(self) -> FBTAKeyInterupt:
    #     return self.__keykill

    @property
    def user_information(self) -> dict:
        return self.__userinfo

    def set_user_information(self, key, val):
        self.__userinfo[key] = val

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, username):
        if not username:
            raise ValueError(':Settings: Username MUST not empty')
        else:
            self.__username = username

    @property
    def cluster_num(self):
        return self.__cluster_num

    @cluster_num.setter
    def cluster_num(self, num):
        if num != 10:
            print(':setting: Recommended cluster=10')
        self.__cluster_num = int(num) if int(num) <= self.__cluster_limit else self.__cluster_limit
        try:
            self.__cluster_num = int(num) if int(num) <= self.__cluster_limit else self.__cluster_limit
        except:
            raise ValueError(':Settings: Cluster Number Not Correct Format')

    @property
    def db_name(self):
        return self.__getDBName()

    @db_name.setter
    def db_name(self, name: str):
        if name == '':
            raise ValueError(':Settings: Database name MUST not empty')
        elif name is None:
            self.__init_db_name()
        else:
            self.__db_name = name
            if 'fbta_' in name:
                # TODO: เนื่องจาก ขก ค่อยมาทำการแบ่ง
                self.__is_user_init_db = True
                self.__dir_path = self.__dir_save_path + self.__dir_save_prefix + name.replace('fbta_', '')

    @property
    def DIR_DETAIL_NEW_ON_DAY(self):
        return self._DIR_DETAIL_NEW_ON_DAY

    @property
    def DIR_DETAIL_NEW_ALL_RUN(self):
        return self._DIR_DETAIL_NEW_ALL_RUN

    def __getDBName(self):
        if not self.__db_name:
            self.is_auto_dbname = True
            return self.__db_prefix + '_' + self.__db_name
        return self.__db_name

    def __autoInit(self):
        self.__init_db_name()
        self.__init_dir_path_name()

    def __init_db_name(self):
        if not self.__is_user_init_db:
            _dir_db_str = '%Y%m%d_%H%M'
            nowDB = datetime.datetime.now().strftime(_dir_db_str)
            self.db_name = self.__db_prefix + '_' + str(nowDB)

    @property
    def renew_index(self):
        return self.__index_renew

    @renew_index.setter
    def renew_index(self, cond=True):
        self.__index_renew = bool(cond)

    def __str__(self):
        _name = str(self.__class__.__name__)
        maxl = len(max(self.__dict__, key=len)) - (len(_name) + 1)
        s = str('')
        pp = '{: <' + str(maxl) + '} = {!r}\n'
        for i in self.__dict__:
            s += pp.format(str(i).replace('_' + _name, ''), self.__dict__.get(i))
        return s

    def __init_dir_path_name(self):

        if not self.__is_user_init_db:
            _dir_dir_str = '%Y%m%d'

            if self.__dir_path_detail == self.DIR_DETAIL_NEW_ALL_RUN:
                _dir_dir_str = '%Y%m%d_%H%M'

            nowDir = datetime.datetime.now().strftime(_dir_dir_str)
            nowDir = self.dir_save_path + self.__dir_save_prefix + nowDir

            self.__dir_path = nowDir
        else:
            self.__dir_path = self.dir_save_path + self.__dir_save_prefix + self.db_name.replace('fbta_', '')

    @property
    def dir_path(self):
        if not self.__dir_path:
            self.__init_dir_path_name()
        return self.__dir_path

    @property
    def dir_save_path(self):
        return self.__dir_save_path

    @dir_save_path.setter
    def dir_save_path(self, dir='./'):
        if not dir:
            self.__dir_save_path = './'
        else:
            self.__dir_save_path = dir[:-1] + '/' if dir[-1] != '/' else dir

    @property
    def dir_path_detail(self):
        return self.__dir_path_detail

    @dir_path_detail.setter
    def dir_path_detail(self, level):
        cond = [self.DIR_DETAIL_NEW_ON_DAY, self.DIR_DETAIL_NEW_ALL_RUN]
        if level not in cond:
            raise ValueError(':Settings: Directory Level Not Correct')
        self.__dir_path_detail = level
        self.__init_dir_path_name()

    @property
    def driver_path(self):
        return self.__driver_path

    @driver_path.setter
    def driver_path(self, dir='./'):
        if not dir:
            raise ValueError(':Settings: Chrome Driver Path Not Correct')
        self.__driver_path = dir[:-1] if dir[-1] == '/' else dir

    @property
    def date_process(self):
        return self.__date_process

    @date_process.setter
    def date_process(self, date: list):
        t_date = [1990, 1, 1]
        if date:
            for i, d in enumerate(date):
                if i == 0:
                    if len(str(d)) == 4:
                        t_date[i] = int(d)
                    else:
                        raise ValueError(':Settings: DateProcess "Year" is not format')
                elif i == 1:
                    if len(str(d)) <= 2 and (0 < int(d) <= 12):
                        t_date[i] = int(d)
                    else:
                        raise ValueError(':Settings: DateProcess "Month" is not format')
                elif i == 2:
                    if len(str(d)) <= 2 and (0 < int(d) <= 31):
                        t_date[i] = int(d)
                    else:
                        raise ValueError(':Settings: DateProcess "Day" is not format')

        self.__date_process = t_date

    @property
    def cluster_limit(self):
        return self.__cluster_limit

    @cluster_limit.setter
    def cluster_limit(self, limit: int):
        try:
            self.__cluster_limit = int(limit)
        except:
            self.__cluster_limit = self.__cluster_limit if self.__cluster_limit else 15

    @property
    def test_step(self):
        return self.__test_step

    @test_step.setter
    def test_step(self, step=None):
        if type(step) == type(None):
            self.__test_step = []
        elif type(step) == list:
            print(f':Settings: Assign Step {step}')
            self.__test_step = step
        else:
            raise ValueError(':Settings: TestStep Value is not NONE or LIST')

    @property
    def password_key(self):
        return self.__file_password_key

    @password_key.setter
    def password_key(self, file):
        if not file:
            ValueError(':Settings: Password KEY file path is empty')
        self.__file_password_key = self.__check_password_file(file, defualt_file=r'./key.key')

    def __check_password_file(self, file=None, defualt_file=r'./password.enc'):
        if not file:
            if not os.path.exists(defualt_file):
                raise FileNotFoundError(f':Settings: {defualt_file} not found')
            return defualt_file
        else:
            if not os.path.exists(file):
                raise FileNotFoundError(f':Settings: {file} not found')
        return file

    @property
    def password_enc(self):
        return self.__file_password_enc

    @password_enc.setter
    def password_enc(self, file):
        if not file:
            ValueError(':Settings: Password KEY file path is empty')
        self.__file_password_enc = self.__check_password_file(file, defualt_file=r'./password.enc')

    @property
    def use_nodeMaster(self) -> bool:
        return self.__use_node_master

    @use_nodeMaster.setter
    def use_nodeMaster(self, cond=True):
        self.__use_node_master = bool(cond)

    @property
    def use_nodeSlave(self) -> bool:
        return self.__use_node_slave

    @use_nodeSlave.setter
    def use_nodeSlave(self, cond=True):
        self.__use_node_slave = bool(cond)

    @property
    def use_nodeMaster_loadCookie(self):
        return self.__use_node_master_cookie

    @use_nodeMaster_loadCookie.setter
    def use_nodeMaster_loadCookie(self, cond=True):
        self.__use_node_master_cookie = bool(cond)

    @property
    def run_fast_all(self):
        return self.__run_fast_all

    @run_fast_all.setter
    def run_fast_all(self, cond=False):
        self.__run_fast_all = bool(cond)

    def __load_ignore_name(self):
        ignore_name = './config/ignore_name.txt'
        name_list = []
        if os.path.exists(ignore_name):
            with open(ignore_name, mode='r') as fo:
                name_list = [str(fr).strip() for fr in fo.readlines()]
            # Remove Empty list
            name_list = [f for f in name_list if f]

        return name_list

    @property
    def ignore_names(self):
        if self.__ignore_name == -1:
            self.__ignore_name = self.__load_ignore_name()
        return self.__ignore_name
