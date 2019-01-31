import datetime
import csv
from sun_riseset_jake import ScrapSunRiseSet

# scrapper init
ssrs = ScrapSunRiseSet(False)

# set vars for scrap
start_date = '2017-04-01'
end_date = '2017-04-02'
address = '충남+천안시+서북구+천안대로+1223-24'

# set vals for scrap
oneday = datetime.timedelta(days=1)
sdt = datetime.datetime.strptime(start_date, '%Y-%m-%d')
edt = datetime.datetime.strptime(end_date, '%Y-%m-%d')

# set module
outfile = open('/home/witlab/sunriseset_output_1.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(outfile)

while sdt <= edt:
    sunrslist = ssrs.scrap(sdt.strftime('%Y-%m-%d'), address)
    csv_writer.writerow(sunrslist)
    ptstr = ''
    for s in sunrslist:
        ptstr += str(s) + ','
    print(ptstr[:-1])
    sdt = sdt + oneday

outfile.close()
ssrs.close()
