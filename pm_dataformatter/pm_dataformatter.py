import pandas as pd
import datetime
import csv
import os

# 원본 데이터 : 에어코리아 확정데이터
# 파일 이름 형식 : yymm.xls -> 파일이름 기반으로 연도 설정하므로 필수로 지켜야함!


def search(dirname):
    # dirname 디렉토리 내의 모든 파일과 디렉토리 이름을 리스트로 반환함
    filelist = []
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        filelist.append(full_filename)
    return filelist


# 파일 이름은 yymm.xls 의 형식이어야함!
def airkorea_pm_xls_to_csv(dirpath: str, outfilepath: str):
    infilelist = search(dirpath)

    for infile in infilelist:
        data = pd.read_excel(infile)
        rows = data.iloc[1:, 0:3]

        print(infile)

        outfile = open(outfilepath, 'a', encoding='utf-8', newline='')
        csv_writer = csv.writer(outfile)

        for i in range(rows.shape[0]):
            row = list(rows.iloc[i])
            datestr = row[0][:6] + str(int(row[0][6:8]) - 1)
            row[0] = datetime.datetime.strptime(datestr, "%m-%d-%H").strftime("20" + infile[-8:-6] + "-%m-%d %H")
            csv_writer.writerow(row)


# airkorea_pm_xls_to_csv('D:/Desktop/pm_ssd', 'D:/Desktop/pm_ssd/pm_ssd.csv')
# airkorea_pm_xls_to_csv('D:/Desktop/pm_shd', 'D:/Desktop/pm_shd/pm_shd.csv')
# airkorea_pm_xls_to_csv('D:/Desktop/pm_bsd', 'D:/Desktop/pm_bsd/pm_bsd.csv')
airkorea_pm_xls_to_csv('D:/Desktop/pm_sgu', 'D:/Desktop/pm_sgu/pm_sgu.csv')
