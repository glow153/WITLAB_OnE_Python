import happybase
from datetime import datetime, timedelta
import pprint

# scan in hbase shell
#

connection = happybase.Connection('210.102.142.14')  # default port : 9090
table = connection.table('natural_light')

startdt = datetime.strptime('2018-11-20 1200', '%Y-%m-%d %H%M')
# startdt = datetime.strptime('2018-03-10 1200', '%Y-%m-%d %H%M')
td = timedelta(days=1)
tm = timedelta(minutes=1)

# for j in range(40):
#     print(j, 'day')
#     for i in range(1440):  # one day
#         strdt = startdt.strftime('%Y-%m-%d %H%M')
#         row = table.row(strdt, ['sp_ird'])
#         count = len(row.keys())
#         if count > 2000:
#             print(strdt, count)
#         startdt += tm

strdt = startdt.strftime('%Y-%m-%d %H%M')
print(strdt)
row = table.row(strdt, ['sp_ird'])

# print dict pretty
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(row)

connection.close()
