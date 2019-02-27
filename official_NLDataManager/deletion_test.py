import happybase
from datetime import datetime, timedelta
import pprint

connection = happybase.Connection('210.102.142.14')
table = connection.table('natural_light')

oneday = timedelta(days=1)
onemin = timedelta(minutes=1)

deletion_target_dt = []

# startdt = datetime.strptime('2017-04-10 0000', '%Y-%m-%d %H%M')
startdt = datetime.strptime('2018-03-23 0000', '%Y-%m-%d %H%M')
for j in range(1440):
    strdt = startdt.strftime('%Y-%m-%d %H%M')
    row = table.row(strdt, ['sp_ird'])
    count = len(row.keys())

    if count > 2000:
        print('delete row :', strdt)
        table.delete(strdt, ['sp_ird'])

    startdt += onemin

    # startdt += oneday

# print dict pretty
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(row)


connection.close()
