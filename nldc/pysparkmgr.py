from mvc.model.singleton import Singleton
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import SQLContext


# 싱글톤을 쓰는 이유 : PySpark에 한번만 접속하여 연결을 유지해야 하기 때문, 중복접속시 에러남
# 따라서 Spark로의 모든 접속은 PySparkManager 싱글톤 객체를 통해서만 수행되어야 함
# 다른 좋은 방법들도 있겠지만 우선은 싱글톤을 활용해보자


class PySparkManager(Singleton):
    sc = None
    nt_srs = None

    def __init__(self):
        self.bs_server_ip = '210.102.142.14'
        self.sc = self.getSparkContext('appName', 'local[*]')
        self.sqlContext = self.getSqlContext()
        self.sundf = self.sqlContext.read.parquet("hdfs:///ds/sun.parquet")

    def getSqlContext(self):
        return SQLContext(self.sc)

    def getSparkContext(self, appName, master):
        if self.sc:
            return self.sc

        conf = SparkConf().setAppName(appName)\
                          .setMaster(master)\
                          .set('spark.local.ip', self.bs_server_ip)\
                          .set('spark.driver.host', self.bs_server_ip)
        return SparkContext(conf=conf)

    def getsrs(self, day):
        rs = self.sundf.select("rise", "set") \
                .where('date = "%s"' % day) \
                .collect()
        return {"rise": str(rs[0][0]),
                "set": str(rs[0][1])}

    def getDF(self, type):
        if type == 'nt_srs':
            if self.nt_srs is None:
                self.nt_srs = self.sqlContext.read.parquet('hdfs:///ds/nt_srs.parquet')
            return self.nt_srs
