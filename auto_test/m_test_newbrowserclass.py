from fbta_browser_selenium import FBTANewBrowser
from fbta_browser_constant import FBTABrowserConstant
from fbta_configs import FBTAConfigs
from fbta_settings import FBTASettings

if __name__ == '__main__':
    s = FBTASettings('fadehara')
    c = FBTAConfigs()
    s.driver_path = r'./Driver/chromedriver_74.exe'
    b = FBTANewBrowser(FBTABrowserConstant.NODE_SLAVE, s, c)
    b.goto('https://google.com')
    b.name = 'master'
    b.save_cookies()
