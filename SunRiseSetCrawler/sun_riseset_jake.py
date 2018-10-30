from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ScrapSunRiseSet:
    baseUrl = 'https://astro.kasi.re.kr:444/life/pageView/9'
    url = ''
    chrome_options = None
    driver = None
    debug = False

    def __init__(self, debug):
        self.debug = debug

        if self.debug:
            print('dbg> init driver...')
        chrome_driver_path = './driver/chromedriver.exe'
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options,
                                       executable_path=chrome_driver_path)
        if self.debug:
            print('dbg> complete!')

    def scrap(self, date, address):
        self.url = self.baseUrl + '?date=' + date + '&address=' + address
        if self.debug:
            print('dbg> request url :', self.url)
        self.driver.get(self.url)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        sunrise = soup.find_all('span', {'class': 'sunrise'})[0].string
        culmination = soup.find_all('span', {'class': 'culmination'})[0].string
        sunset = soup.find_all('span', {'class': 'sunset'})[0].string

        sr = sunrise[0:2] + ':' + sunrise[4:-1]
        cul = culmination[0:2] + ':' + culmination[4:-1]
        ss = sunset[0:2] + ':' + sunset[4:-1]

        if self.debug:
            print('dbg>', date, sr, cul, ss)

        return [date, sr, cul, ss]

    def close(self):
        if self.debug:
            print('dbg> close!')
        self.driver.close()


if __name__ == '__main__':
    date = '2018-03-20'
    address = '충남+천안시+서북구+천안대로+1223-24'

    ssrs = ScrapSunRiseSet(False)

    print(ssrs.scrap(date, address))

    ssrs.close()
