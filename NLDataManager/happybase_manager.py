import happybase
import pprint
from nldc_entity.cas_entity import CasEntity


class NLDataManager:
    _server_addr = ''
    _tablename = ''
    _hb_conn = None
    _hb_table_conn = None

    def __init__(self, addr: str, tablename: str):
        self._server_addr = addr
        self._tablename = tablename

    def connect(self):
        self._hb_conn = happybase.Connection(self._server_addr)
        self._hb_table_conn = self._hb_conn.table(self._tablename)
        try:
            self._hb_table_conn.counter_get('1', '1')
        except Exception:
            self.create_table()

    def disconnect(self):
        self._hb_conn.close()

    def _getmerge_data2dict(self, datedir):
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
            mc = nle.get_dict('measurement conditions')
            res = nle.get_dict('results')
            gi = nle.get_dict('general information')
            uv = nle.get_dict('uv')
            sp = nle.get_dict('data')

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

    def _hb_insert_nle(self, dict_nlentity: dict):
        rowkeyset = dict_nlentity.keys()
        for rowkey in rowkeyset:
            self._hb_table_conn.put(rowkey, dict_nlentity[rowkey])

        self._hb_conn.close()

    def create_table(self):
        dict_families = {'measurement_conditions': dict(),
                         'results': dict(),
                         'general_information': dict(),
                         'sp_ird': dict(),
                         'uv': dict()}

        self._hb_conn.create_table(self._tablename, dict_families)

        table = self._hb_conn.table(self._tablename)

    def insert_datedir(self, datedir: str):
        dict_dailydata = self._getmerge_data2dict(datedir)
        self._hb_insert_nle(dict_dailydata)

    def select_datehm(self, dhm: str):  # dhm format: '%Y-%m-%d %H%M'
        row = self._hb_table_conn.row(dhm, ['sp_ird'])

        # print dict pretty
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(row)


if __name__ == "__main__":
    nldmgr = NLDataManager('210.102.142.14', 'natural_light')
    nldmgr.connect()
    nldmgr.insert_datedir('D:/Desktop/2018 natural/20181120')
    nldmgr.select_datehm('2018-11-20 1200')

