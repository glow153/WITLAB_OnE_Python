from nldc_entity.cas_entity import CasEntity
import csv


rootdir = 'D:/Desktop/rat'
outputFileName = rootdir.split('/')[-1] + '_output.csv'

flist = CasEntity.search(rootdir)
outfile = open(rootdir + '/' + outputFileName, 'w', encoding='utf-8', newline='')
# outfile = open('D:/Desktop/tmp/output.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(outfile)

csv_writer.writerow(['time', 'illum', 'uvb', 'euvb', 'uva', 'euva', 'auv'])

for fname in flist:
    # print('>>' + fname)
    try:
        entity = CasEntity(fname)
        entity_row = [entity.get_datetime(tostr=True),
                             entity.get_element('Photometric'),
                             entity.get_element('uvb'),
                             entity.get_element('euvb'),
                             entity.get_element('uva'),
                             entity.get_element('euva'),
                             entity.get_element('hazard_uv'),
                             ]
        print(entity_row)
        csv_writer.writerow(entity_row)
    except AttributeError:
        continue

outfile.close()
