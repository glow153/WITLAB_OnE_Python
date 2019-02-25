from nldc_entity.cas_entity import CasEntity
import csv


rootdir = 'C:/Users/JakePark/OneDrive/experiment/jgc/uv_band_prototype_01/calibration_7_nl/20190221'
outputFileName = rootdir.split('/')[-1] + '_output.csv'

flist = CasEntity.search(rootdir)
outfile = open(rootdir + '/' + outputFileName, 'w', encoding='utf-8', newline='')
# outfile = open('D:/Desktop/tmp/output.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(outfile)

csv_writer.writerow(['time', 'int_time', 'ccdtemp', 'uvi', 'uvb', 'euvb', 'uva', 'euva', 'duv', 'auv'])

for fname in flist:
    # print('>>' + fname)
    try:
        entity = CasEntity(fname)
        entity_row = [entity.get_datetime(tostr=True).split(' ')[1],
                      entity.get_element('IntegrationTime'),
                      entity.get_element('CCDTemperature'),
                      entity.get_element('uvi'),
                      entity.get_element('uvb'),
                      entity.get_element('euvb'),
                      entity.get_element('uva'),
                      entity.get_element('euva'),
                      entity.get_element('duv'),
                      entity.get_element('auv'),
                      ]
        print(entity_row)
        csv_writer.writerow(entity_row)
    except AttributeError:
        continue

outfile.close()
