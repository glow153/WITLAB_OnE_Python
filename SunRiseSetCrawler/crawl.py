import sun_riseset_jake
import datetime


address = '충남+천안시+서북구+천안대로+1223-24'
risesetTimeList = []
ssrs = sun_riseset_jake.ScrapSunRiseSet(True)

startDatetime = datetime.datetime.strptime('2017-03-01', '%Y-%m-%d')

while True:
    strDt = startDatetime.strftime('%Y-%m-%d')
    entity = ssrs.scrap(strDt)
    print(entity)
    risesetTimeList.append(entity)
    if strDt == '2018-06-30':
        break
    startDatetime += datetime.timedelta(days=1)

for rstime in risesetTimeList:
    strrow = ''
    for item in rstime:
        strrow += (item + ',')
    print(strrow[:-1])


