from typing import List, Optional

from fbta_global_database_manager import FBTADBManager
from fbta_03_history_download_method import FBTAHistoryDownloaderMethod
from fbta_main_worker import FBTAMainWorker
from fbta_node_master import FBTANodeMaster
from fbta_log import log
from parsel import Selector


class FBTAPhotosDownloadWorker(FBTAMainWorker):
    def __init__(self, node_master: FBTANodeMaster, db: FBTADBManager):
        self.__node_master = node_master
        self.__db = db

        FBTAMainWorker.__init__(self, node_master)
        # self.__activity: FBTAHistoryDownloaderMethod = FBTAHistoryDownloaderMethod.NONE

    def after_init(self):
        pass
        # self.__activity = FBTAHistoryDownloaderMethod(self.__node_master, self.worker_browser, self.__db)
        # self.__activity.slave_name = self.name

    def slave_method(self, docs):
        self.downloadSpliter(docs)

    def downloadSpliter(self, docsOnces):
        bs = Selector(docsOnces['source'])

        gg: List[Optional[Selector]] = bs.xpath("//div[@data-ft]")
        # print(gg)
        if len(gg) == 1:
            print('jjj',[x.attrib['data-ft'] for x in gg])

        # if len(gg) == 0:
        #     print(len(pp), docsOnces['url'])
        #     print(pp)
        #     print(pp[0].get('data-ft'))
        #     print()
        # if len(gg) == 1:
        #     print(len(pp), docsOnces['url'])
        #     # print(pp)
        #     pprint(pp[0].get('data-ft'))
        #     print()
        # if len(gg) > 0:
        #     hasArticle = False
        #     for i, p in enumerate(gg):
        #         if p.get('role') == 'article':
        #             # print('+++',p)
        #             jss: dict = json.loads(p.get('data-ft'))
        #             # print(len(pp), docsOnces['url'])
        #             url0 = 'https://m.facebook.com/'
        #             url = url0 + jss.get('top_level_post_id')
        #             atta = jss.get('attached_story_attachment_style')
        #             if atta:
        #                 if atta == 'photo':
        #                     print('ASAS', atta)
        #                     # print(url)
        #                     # pprint(url0 + jss['photo_id'])
        #                     rrrr = self.__photosDownload.downloadPhoto(url0 + jss['photo_id'], docsOnces, jss)
        #                     # print(rrrr)
        #                     # exit()
        #
        #                     # exit()
        #             elif jss.get('story_attachment_style'):
        #                 pass
        #                 # print('PA', jss.get('story_attachment_style'))
        #             else:
        #                 pass
        #                 # print('ERROR')
        #                 # print(jss)
        #
        #             hasArticle = True
        #     if not hasArticle and len(gg) > 0:
        #         pass
        #         # i.e. ME like Post Share
        #
        #         # print(len(pp), docsOnces['url'])
        #         # print(gg)
        #
        #         # print()
        # if len(gg) == 0:
        #     # i.e Note
        #     pass
