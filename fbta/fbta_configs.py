class FBTAConfigs:
    def __init__(self):
        self.window_size_width = 780
        self.window_size_height = 800

        self.__facebook_url_main = 'https://m.facebook.com'
        self.__db_collection_stat = 'statistic'
        self.__db_collection_log = 'log'
        self.__db_collection_yearbox_name = '00_yearbox_page'
        self.__db_collection_page_name = '01_activity_page'
        self.__db_collection_card_name = '02_card_page'
        self.__db_collection_post_name = '03_post_page'
        self.__db_collection_photo_name = '04_photo_page'
        self.__db_collection_05_album_count_name = '05_album_count'
        self.__time_retry_addCookie = 10
        self.__time_retry_connectError = 30
        self.time_master_lock_cooldown = 2

        self.__dir_seq_01_activity = '01_activity'
        self.__dir_seq_02_story = '02_story_screenshot'
        self.__dir_seq_03_photoScreenshot = '03_photo_ss'
        self.__dir_seq_03_photos = '03_photos'

        self.timeout_waiting_list = 50



    @property
    def db_collection_00_yearbox_name(self):
        return self.__db_collection_yearbox_name

    @property
    def dir_seq_01_Activity(self):
        return self.__dir_seq_01_activity

    @property
    def dir_seq_02_story(self):
        return self.__dir_seq_02_story

    @property
    def dir_seq_03_photoScreenshot(self):
        return self.__dir_seq_03_photoScreenshot

    @property
    def dir_seq_03_photos(self):
        return self.__dir_seq_03_photos

    @property
    def db_collection_01_page_name(self) -> str:
        return self.__db_collection_page_name

    @property
    def db_collection_02_card_name(self) -> str:
        return self.__db_collection_card_name

    @property
    def db_collection_03_post_name(self) -> str:
        return self.__db_collection_post_name

    @property
    def db_collection_04_photo_name(self) -> str:
        return self.__db_collection_photo_name

    @property
    def db_collection_05_album_count_name(self) -> str:
        return self.__db_collection_05_album_count_name

    @property
    def db_collection_stat(self) -> str:
        return self.__db_collection_stat

    @property
    def facebook_url_main(self) -> str:
        return self.__facebook_url_main

    @property
    def time_retry_addCookie(self):
        return self.__time_retry_addCookie

    @property
    def time_retry_connectError(self):
        return self.__time_retry_connectError

    def __str__(self):
        _name = str(self.__class__.__name__)
        maxl = len(max(self.__dict__, key=len)) - (len(_name) + 3)
        s = str('')
        pp = '{: <' + str(maxl) + '} = {!r}\n'
        for i in self.__dict__:
            s += pp.format(str(i).replace('_' + _name + '__', ''), self.__dict__.get(i))
        return s
