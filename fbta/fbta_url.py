from fbta_configs import FBTAConfigs
from fbta_settings import FBTASettings


class FBTAUrl:
    NONE = None

    def __init__(self, settings: FBTASettings, global_configs: FBTAConfigs):
        self.configsClass = global_configs
        self.settingsClass = settings
        self.values = {}

        self.__updateValue()

        self.urlList = {
            'main': '{url-main}',
            'activity': '{url-main}/{username}/allactivity',
            'language': '{url-main}/__settings/language/',
            'profile': '{url-main}/me'
        }

    def setUsername(self, username):
        self.values['username'] = username

    def __updateValue(self):
        self.values['url-main'] = self.configsClass.facebook_url_main
        self.values['username'] = self.settingsClass.username

    def __getUrlList(self, key: str) -> str:
        return self.urlList[key].format(**self.values)

    def __getMainUrl(self) -> str:
        return self.__getUrlList('main')

    def getUrlFacebook(self) -> str:
        return self.__getMainUrl()

    def getUrlLangugeSelect(self) -> str:
        return self.__getUrlList('language')

    def getUrlActivityLog(self) -> str:
        return self.__getUrlList('activity')

    def getUrlProfile(self) -> str:
        return self.__getUrlList('profile')

    def getUrlWithMain(self, url: str) -> str:
        prefix = '' if url and url[0] == '/' else '/'
        return self.__getMainUrl() + prefix + str(url)
