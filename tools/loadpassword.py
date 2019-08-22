class LoadPassword:
    def __init__(self, dir):
        self.password = ''
        self.dir = dir


    def __getFileFromPath(self):
        import os
        password = ''
        if os.path.exists(self.dir):
            with open(self.dir, mode='r', encoding='utf8') as fo:
                password = fo.read()

        self.password = password


    def getPassword(self)->str:
        self.__getFileFromPath()
        return self.password