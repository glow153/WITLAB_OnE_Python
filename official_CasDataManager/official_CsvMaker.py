from nldc_entity.cas_entity import CasEntity
import csv


rootdir = 'D:\Downloads\kk_181030_디퓨저추가'
outputFileName = 'output.csv'

flist = CasEntity.search(rootdir)
# outfile = open(rootdir + '/' + outputFileName, 'w', encoding='utf-8', newline='')
outfile = open('D:/Desktop/output.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(outfile)

csv_writer.writerow(['time', 'illum', 'cct', 'swr', 'narr'])

for fname in flist:
    print('>>' + fname)
    entity = CasEntity(fname)
    csv_writer.writerow([entity.get_datetime(tostr=True),
                         entity.get_element('Photometric'),
                         entity.get_element('CCT'),
                         entity.get_element('swr'),
                         entity.get_element('narr')
                         ])

outfile.close()
