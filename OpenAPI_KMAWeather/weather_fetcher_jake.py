import json
from requests import get as req_get
import datetime
import csv


def replace_base_datetime(ctime):
    h = ctime.hour

    if h < 2:
        ctime += datetime.timedelta(days=-1)
        ctime = ctime.replace(hour=23)
    else:
        ctime = ctime.replace(hour=(h - ((h + 1) % 3)))

    return ctime


def get_datetime_sa(ctime):
    date = ctime.strftime('%Y%m%d')
    time = ctime.strftime('%H') + '00'
    return date, time


def get_weather_dict(sadt, nx=63, ny=111):
    base_url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData'
    service_key = 'v9ArtjlS3sC0ObVFeayEo6hMm9lTDc0Yizsquek9IFEadCQvSkMonOBeklG2EJjmcWrIwPnNyokV6Nsn3faApA%3D%3D'

    url = base_url + '?serviceKey=' + service_key \
          + '&base_date=' + sadt[0] \
          + '&base_time=' + sadt[1] \
          + '&nx=' + str(nx) \
          + '&ny=' + str(ny) \
          + '&numOfRows=20&_type=json'

    response_json = req_get(url)
    weather = json.loads(response_json.text)
    return weather


def log_weather():
    outFileName = '/root/openapi/logdata.csv'
    col = ['POP', 'PTY', 'R06', 'REH', 'S06', 'SKY', 'T3H', 'UUU', 'VEC', 'VVV', 'WSD']
    now = datetime.datetime.now()
    base_datetime = replace_base_datetime(now)
    base_datetime_sa = get_datetime_sa(base_datetime)

    weather = get_weather_dict(base_datetime_sa)
    wdata = weather['response']['body']['items']['item']
    fcstdata = {}
    fcstDateTime = ''

    for item in wdata:
        dt = base_datetime + datetime.timedelta(hours=4)
        if str(item['fcstTime']) != dt.strftime('%H00'):
            continue
        else:
            fcstDateTime = str(item['fcstDate']) + ' ' + str(item['fcstTime'])
            fcstdata[item['category']] = item['fcstValue']
    
    record = [fcstDateTime]
    for colname in col:
        try:
            print(colname, ':', fcstdata[colname])
            record.append(fcstdata[colname])
        except KeyError:
            record.append('x')
    print(record)
    
    f = open(outFileName, 'a', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(record)
    wr.close()

