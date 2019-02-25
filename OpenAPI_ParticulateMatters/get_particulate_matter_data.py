import requests
import json
import csv
import datetime
import os


class ParticulateMatterFetcher:
    service_key = 'zo2rUB1wM3I11GNZFDuB84l4C94PZjP6cEb4qEff%2B94h83%2Fihaj1JJS75%2Bm0uHdFCchJw7SyGE0HZgKiZDpq%2FA%3D%3D'
    url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'

    @staticmethod
    def datetime_corrector(sDatetime):
        sdate = sDatetime.split()[0]
        stime = sDatetime.split()[1]
        dtdate = datetime.datetime.strptime(sdate, '%Y-%m-%d')
        if stime[:2] == '24':
            oneday = datetime.timedelta(days=1)
            dtdate += oneday
            sdate = dtdate.strftime('%Y-%m-%d')
            stime = '00' + stime[2:]
        return sdate + ' ' + stime

    def fetchinfo(self, station='nearest', term='daily', ret='dict'):
        queryParams = '?ServiceKey=' + self.service_key
        if station == 'nearest':
            queryParams += '&stationName=성성동'
        else:
            queryParams += '&stationName=' + station

        if term == 'daily':
            queryParams += '&dataTerm=DAILY&numOfRows=25'
        elif term == 'month':
            queryParams += '&dataTerm=MONTH&numOfRows=744'
        elif term == '3month':
            queryParams += '&dataTerm=3MONTH&numOfRows=2232'

        queryParams += '&_returnType=json'

        if ret == 'str':
            return (requests.get(self.url + queryParams)).text
        else:
            return json.loads(requests.get(self.url + queryParams).text)

    def logcsv(self, dict, fullpath):
        outfile = open(fullpath, 'w', encoding='utf-8', newline='')
        csv_writer = csv.writer(outfile)
        colume_name = ['dataTime', 'pm10Value', 'pm25Value']
        if os.path.getsize(fullpath) > 0:
            csv_writer.writerow(colume_name)
        lsData = dict['list']
        lsData_rev = []
        # reverse row list
        for i in reversed(range(len(lsData))):
            lsData_rev.append(lsData[i])

        for item in lsData_rev:
            row = []
            for key in colume_name:
                row.append(item[key])
            row[0] = self.datetime_corrector(row[0])
            csv_writer.writerow(row)


if __name__ == '__main__':
    path = 'D:/Desktop'
    filename = 'pm_cheonan-new.csv'

    fp = ParticulateMatterFetcher()
    # dict_data = fp.fetchinfo(station='태안읍', term='3month')
    dict_data = fp.fetchinfo(station='성성동', term='3month')
    fp.logcsv(dict_data, path + '/' + filename)

    requests.post('', )