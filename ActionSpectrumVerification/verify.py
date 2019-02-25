from nldc_entity.cas_entity import CasEntity
import csv

dirname = 'C:/Users/JakePark/OneDrive/ActionSpectrumCalcVerification'
infilename = 'sample.ISD'

cas_entity = CasEntity(dirname + '/' + infilename)
outfile = open(dirname + '/script_output.csv', 'wt', encoding='utf-8', newline='')
csv_writer = csv.writer(outfile)

# todo: sample로부터 EUV, AUV 산출
csv_writer.writerow(['uva', 'uvb', 'euva', 'euvb', 'duv', 'auv'])
csv_writer.writerow([cas_entity.get_element('uva'),
                     cas_entity.get_element('uvb'),
                     cas_entity.get_element('euva'),
                     cas_entity.get_element('euvb'),
                     cas_entity.get_element('duv'),
                     cas_entity.get_element('hazard_uv')
                     ])

outfile.close()

