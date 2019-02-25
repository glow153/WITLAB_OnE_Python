from PyQt5.QtWidgets import QMessageBox

from pysparkmgr.pysparkmgr import PySparkManager
from pysparkmgr.singleton import Singleton


class NLDailyDataset(Singleton):
    factor_list = ['illum', 'cct', 'swr', 'UVA', 'UVB', 'EUVA', 'EUVB', 'EUVB_ratio', 'UVI']

    def __init__(self):
        # get PySparkManager
        self.pysparkmgr = PySparkManager()
        self.initDF()

    def initDF(self):
        try:
            self.df_nt.printSchema()
        except Exception:
            self.df_nt = self.pysparkmgr \
                .getSqlContext().read.parquet('hdfs:///ds/nt.parquet')
        try:
            self.df_uv.printSchema()
        except Exception:
            self.df_uv = self.pysparkmgr \
                .getSqlContext().read.parquet('hdfs:///ds/uv.parquet')

    def getDataset(self, type, day, filter=None):
        if type not in self.factor_list:
            QMessageBox.question(self, 'Factor Select Error',
                                 '데이터 요소 선택이 잘못되었습니다.\n' + type,
                                 QMessageBox.Ok, QMessageBox.Ok)
