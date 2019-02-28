import requests
from bs4 import BeautifulSoup


url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/get24DivisionsInfo'
service_key = ''
year = 2017
month = 1


for i in range(12):
    strMonth = str(month) if len(str(month)) == 2 else '0' + str(month)

    param = '?solYear=' + str(year) + '&solMonth=' + strMonth + '&ServiceKey=' + service_key

    # print(url + param)
    doc = requests.get(url + param)

    soup = BeautifulSoup(doc.text, 'html.parser')

    for item in soup.findAll('item'):
        datename = item.datename.text
        locdate = item.locdate.text
        print('datename:', datename, ', locdate:', locdate)

    month += 1



