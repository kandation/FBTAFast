import os

from fbta.fbta_configs import FBTAConfigs
from fbta.fbta_settings import FBTASettings


class FBTAMkdir:
    def __init__(self, settings: FBTASettings, configs: FBTAConfigs):
        self.__settingsClass = settings
        self.__configsClass = configs

    def startProjectDir(self):
        self.__make_dir(self.__settingsClass.dir_path)
        # self.__make_dir(self.__settingsClass.getProjectPath(self.__configsClass.dir_seq_01_Activity))
        # self.__make_dir(self.__settingsClass.getProjectPath(self.__configsClass.dir_seq_02_story))
        # self.__make_dir(self.__settingsClass.getProjectPath(self.__configsClass.dir_seq_03_photoScreenshot))
        self.__make_dir(self.__settingsClass.getProjectPath(self.__configsClass.dir_seq_03_photos))

    def __make_dir(self, dirname):
        print(f':Mkdir: Generate Directory {dirname}')
        current_path = os.getcwd()
        path = os.path.join(current_path, dirname)
        if not os.path.exists(path):
            os.makedirs(path)
