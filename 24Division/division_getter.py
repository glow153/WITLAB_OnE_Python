import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


class DivisionGetter:
    url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/get24DivisionsInfo'
    service_key = ''
    division = {}

    def __init__(self, service_key):
        self.service_key = service_key

    def get_monthly(self, year: int, month: int):
        # month string formatting
        strMonth = str(month) if len(str(month)) == 2 else '0' + str(month)
        # make query parameter
        query_param = '?solYear=' + str(year) + '&solMonth=' + strMonth + '&ServiceKey=' + self.service_key

        # send get method
        doc = requests.get(self.url + query_param)
        # parse xml
        soup = BeautifulSoup(doc.text, 'html.parser')

        # find element
        for item in soup.findAll('item'):
            datename = item.datename.text
            locdate = item.locdate.text
            self.division[locdate] = datename

    def get_yearly(self, year: int):
        for i in range(1, 13):
            self.get_monthly(year, i)

    def get_division(self):
        return self.division

    def what_is_the_division_of_this_day(self, date):
        oneday = timedelta(days=1)
        objdt = datetime.strptime(date, '%Y%m%d')
        divday_list = list(self.division.keys())
        divday_list.sort()

        for i in range(len(divday_list) - 2):
            objdt_left = datetime.strptime(divday_list[i], '%Y%m%d')
            objdt_right = datetime.strptime(divday_list[i+1], '%Y%m%d')

            # print(date, ':',
            #       divday_list[i], '(', self.division[divday_list[i]], ') ~',
            #       divday_list[i+1], '(', self.division[divday_list[i+1]], ')')

            if divday_list[i] == date:
                return self.division[divday_list[i]]
            elif divday_list[i] < date < divday_list[i+1]:
                td = objdt_right - objdt_left
                # print('objdt_right - objdt_left =', td.days)
                # print('thr=', (objdt_left + timedelta(days=int(td.days/2))).strftime('%Y%m%d'))
                if date < (objdt_left + timedelta(days=int(td.days/2))).strftime('%Y%m%d'):
                    return self.division[divday_list[i]]
                else:
                    return self.division[divday_list[i+1]]

            objdt += oneday

        return 'no data'


if __name__ == "__main__":
    key = ''
    dg = DivisionGetter(key)
    dg.get_yearly(2017)
    dg.get_yearly(2018)
    dg.get_yearly(2019)
    # print(dg.get_division())
    print(dg.what_is_the_division_of_this_day('20190620'))
