from nldc_entity.cas_entity import CasEntity
from nldc_entity.ref_func import *
import csv

dirname = 'C:/Users/JakePark/OneDrive/ActionSpectrumCalcVerification'
infilename = 'sample.ISD'

cas_entity = CasEntity(dirname + '/' + infilename)
outfile = open(dirname + '/wl_output.csv', 'wt', encoding='utf-8', newline='')
csv_writer = csv.writer(outfile)

# todo: sample의 분광 파장마다 가중치 구해서 csv로 산출하기
wllist = list(cas_entity.get_dict('data').keys())
print(wllist)

# write header
csv_writer.writerow(['wl', 'f_ery', 'f_vitd', 'f_auv'])

# write table
for wl in wllist:
    csv_writer.writerow([wl,
                         erythemal_action_spectrum(wl),
                         vitd_weight_func_interpolated(wl),
                         actinic_uv_weight_func(wl, False),
                         ])

outfile.close()

