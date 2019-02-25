import datetime
import weather_fetcher_jake as wfj

for i in range(0, 24):
    if i < 10:
        hm = '0' + str(i) + '00'
    else:
        hm = str(i) + '00'
    dt = wfj.replaceBaseDatetime(datetime.datetime.strptime(hm, '%H%M'))
    print(dt.strftime('%H00'))

