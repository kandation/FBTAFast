import pickle


def loadCookies(dir='./'):
    cookies = pickle.load(open(dir + "fbta_cookies_old.pkl", "rb"))
    for cookie in cookies:
        glova = ''
        for c in cookie:
            stt = '{name}={val}; '.format(name=c,val=cookie[c])
            glova += stt
        print(glova)

    print('FBTABrowser Load Cookie OK')


if __name__ == '__main__':
    loadCookies()