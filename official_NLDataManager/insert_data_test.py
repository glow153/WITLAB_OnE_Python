import happybase
from nldc_entity.cas_entity import CasEntity
import pprint


# spectral data insertion process
# 1. local 에 있는 CAS data를 dict로 mapping
# 2. dict 만들기 => time : {'col_family_name':'key1' : val1, 'col_family_name':'key2' : val2, ...}
# 3. put


def getmerge_data2dict(datedir):
    flist = CasEntity.search(datedir)
    dict_merged_sp = {}

    # make list and dict
    for fname in flist:

        # get nl entity obj
        nle = CasEntity(fname)

        try:
            datetime = nle.get_datetime(tostr=True)[:-3].replace(':', '')
        except TypeError or AttributeError:
            continue
        print(datetime)

        # get dict from nl entity
        mc = nle.get_category('measurement conditions')
        res = nle.get_category('results')
        gi = nle.get_category('general information')
        uv = nle.get_category('uv')
        sp = nle.get_category('data')

        # add column family to key
        dict_merged_sp[datetime] = dict()
        for k in mc.keys():
            dict_merged_sp[datetime]['measurement_conditions:' + str(k)] = str(mc[k])

        for wl in sp.keys():
            dict_merged_sp[datetime]['sp_ird:' + str(wl)] = str(sp[wl])

        for k in res.keys():
            dict_merged_sp[datetime]['results:' + str(k)] = str(res[k])

        for k in gi.keys():
            dict_merged_sp[datetime]['general_information:' + str(k)] = str(gi[k])

        for k in uv.keys():
            dict_merged_sp[datetime]['uv:' + str(k)] = str(uv[k])

    return dict_merged_sp


def hb_insertData(dict_nlentity):
    connection = happybase.Connection('210.102.142.14')
    table = connection.table('natural_light')

    rowkeyset = dict_nlentity.keys()
    for rowkey in rowkeyset:
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(dict_daily_sp)

        table.put(rowkey, dict_nlentity[rowkey])

    connection.close()


rootdir = 'D:/Desktop/2018 natural'
datelist = CasEntity.search(rootdir)

count = 0
for datedir in datelist:
    date = datedir.split('\\')[1]
    # if date >= '180315':
    # progress(count, len(datelist)*2, 'make daily sp to dict' + date)
    # get merged daily sp dict
    dict_dailydata = getmerge_data2dict(datedir)
    # try:
    #     dict_dailydata = getmerge_data2dict(datedir)
    # except TypeError:
    #     continue
    # except AttributeError:
    #     continue
    count += 1

    # progress(count, len(datelist)*2, 'input daily sp to HBase')
    # debug print
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(dict_dailydata)

    # insert data to hbase
    hb_insertData(dict_dailydata)

    count += 1

# progress(count, len(datelist)*2, 'input daily sp to HBase')
print('\ncompleted!')

