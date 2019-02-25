import datetime
import csv
import os


class CasEntity(object):
    __measurement_conditions = {}
    __results = {}
    __general_information = {}
    __data = {}
    __uv = {}
    objDatetime = None

    def __init__(self, fname):
        isdfile = open(fname, 'rt', encoding='utf-8', errors='ignore')
        valid = self.__map_data(isdfile)
        isdfile.close()

        if valid:
            # print(fname + ' is valid file')
            datatable = self.get_dict_to_list(self.__data)
            self.__set_additional_data(datatable)
            self.__set_uv_dict(datatable)
            self.objDatetime = self.__parse_objdt(
                self.__general_information['Date'] + ' ' + self.__general_information['Time'])

    def __map_data(self, file):
        line = file.readline()
        linetype = 0

        if line.strip() != '[Curve Information]':
            return False

        while line:
            line = line.strip()
            if line == '[Measurement Conditions]':
                linetype = 1
            elif line == '[Results]':
                linetype = 2
            elif line == '[General Information]':
                linetype = 3
            elif line == 'Data':
                linetype = 4
            else:
                # try:
                if line.find('=') != -1:
                    strKey, strValue = line.split('=')
                    key = strKey.strip()
                    strValue = strValue.strip()
                    endidx = strKey.find('[')
                    if endidx != -1:
                        key = key[:endidx].strip()
                    try:
                        value = float(strValue)
                    except ValueError:
                        value = strValue

                elif line.find('\t') != -1:
                    strKey, strValue = line.split('\t')
                    key = float(strKey.strip())
                    value = float(strValue.strip())
                else:
                    line = file.readline()
                    continue
                # except ValueError:
                #     line = file.readline()
                #     continue

                # print(key, value)

                if linetype == 1:
                    self.__measurement_conditions[key] = value

                elif linetype == 2:
                    self.__results[key] = value

                elif linetype == 3:
                    self.__general_information[key] = value

                elif linetype == 4:
                    self.__data[float(key)] = value

                else:  # type == 0
                    pass

            line = file.readline()
        return True

    def __set_additional_data(self, datatable):
        bird_vis = self.get_ird(datatable, 380, 780)
        bird_sw = self.get_ird(datatable, 380, 480)
        bird_mw = self.get_ird(datatable, 480, 560)
        bird_lw = self.get_ird(datatable, 560, 780)
        bird_narrow = self.get_ird(datatable, 446, 477)

        if bird_vis == 0:
            self.__results['swr'] = 0
            self.__results['mwr'] = 0
            self.__results['lwr'] = 0
            self.__results['narr'] = 0
        else:
            self.__results['swr'] = bird_sw / bird_vis
            self.__results['mwr'] = bird_mw / bird_vis
            self.__results['lwr'] = bird_lw / bird_vis
            self.__results['narr'] = bird_narrow / bird_vis

    def __set_uv_dict(self, datatable):
        # calc bb ird of uv
        # self.__uv['uv_general_info'] = {
        #     'unit': 'W/m2',
        # }
        # self.__uv['integration_range'] = {
        #     'tuv': [280, 400],
        #     'uva': [315, 400],
        #     'uvb': [280, 315],
        #     'euv': [280, 400],
        #     'euva': [315, 400],
        #     'euvb': [280, 315],
        #     'duv': [280, 400],
        # }
        self.__uv['tuv'] = self.get_ird(datatable, 280, 400)
        self.__uv['uva'] = self.get_ird(datatable, 315, 400)
        self.__uv['uvb'] = self.get_ird(datatable, 280, 315)
        self.__uv['euv'] = self.get_ird(datatable, 280, 400, weight_func='ery')
        self.__uv['euva'] = self.get_ird(datatable, 315, 400, weight_func='ery')
        self.__uv['euvb'] = self.get_ird(datatable, 280, 315, weight_func='ery')
        self.__uv['uvi'] = self.__uv['euv'] * 40
        self.__uv['duv'] = self.get_ird(datatable, 280, 400, weight_func='vitd')

        if self.__uv['euv'] == 0:
            self.__uv['euva_ratio'] = 0
            self.__uv['euvb_ratio'] = 0
        else:
            self.__uv['euva_ratio'] = self.__uv['euva'] / self.__uv['euv']
            self.__uv['euvb_ratio'] = self.__uv['euvb'] / self.__uv['euv']

        self.__uv['hazard_uv'] = self.get_ird(datatable, 200, 400, weight_func='uv_hazard', alg='trapezoid')

    def __parse_objdt(self, strdt):
        return datetime.datetime.strptime(strdt, '%m/%d/%Y %I:%M:%S %p')

    def get_datetime(self, tostr=False):
        if tostr:
            return self.objDatetime.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return self.objDatetime

    def get_json(self, *args):
        import json
        dict_json = {}

        if 'measurement conditions' in args:
            dict_json['measurement conditions'] = self.__measurement_conditions
        if 'results' in args:
            dict_json['results'] = self.__results
        if 'general information' in args:
            dict_json['general information'] = self.__general_information
        if 'data' in args:
            dict_json['data'] = self.__data
        if 'uv' in args:
            dict_json['uv'] = self.__uv

        return json.dumps(dict_json, indent=4)

    def get_dict(self, item='all'):
        if item == 'measurement conditions':
            return self.__measurement_conditions
        elif item == 'results':
            return self.__results
        elif item == 'general information':
            return self.__general_information
        elif item == 'data':
            return self.__data
        elif item == 'uv':
            return self.__uv

        elif item == 'all':
            return {
                'measurement conditions': self.__measurement_conditions,
                'results': self.__results,
                'general information': self.__general_information,
                'data': self.__data,
                'uv': self.__uv
            }

        else:
            return None

    @staticmethod
    def get_dict_to_list(dict_src, kv=True):
        retlist = []
        for key in dict_src.keys():
            if kv:
                retlist.append([key, dict_src[key]])
            else:
                retlist.append(dict_src[key])
        return retlist

    def get_element(self, item=None):
        keyset_mc = self.__measurement_conditions.keys()
        keyset_re = self.__results.keys()
        keyset_gi = self.__general_information.keys()
        keyset_da = self.__data.keys()
        keyset_uv = self.__uv.keys()

        if item in keyset_mc:
            return self.__measurement_conditions[item]
        elif item in keyset_re:
            return self.__results[item]
        elif item in keyset_gi:
            return self.__general_information[item]
        elif item in keyset_da:
            return self.__data[item]
        elif item in keyset_uv:
            return self.__uv[item]
        else:
            return None

    @staticmethod
    def search(dirname):
        # dirname 디렉토리 내의 모든 파일과 디렉토리 이름을 리스트로 반환함
        filelist = []
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            filelist.append(full_filename)
        return filelist

    @staticmethod
    def get_ird(table, range_val1, range_val2, weight_func='none', alg='rect'):
        # 분광 데이터 테이블로부터 특정 범위에 대한 광파장 복사량(broadband irradiance)을
        # float 단일값으로 반환 (광파장복사량 == 적산 값)
        # range_val1, range_val2 : 적분구간 시작, 끝 값
        # table : get_dict_to_list()로부터 생성된 분광 데이터 테이블(list)
        # weight_func : 가중함수 선택, 홍반가중함수('ery'), 비타민 d 가중함수('vitd'), 없음('none')
        # alg : 적분 알고리즘 선택, 기본값('rect')은 직사각형 공식, 'trapezoid' 로 설정하면 사다리꼴 공식 적용

        broadband_ird = 0

        # for i in range(len(table) - 1):
        index = 0

        for i in range(len(table) - 2):
            wll = float(table[i][0])
            irdl = float(table[i][1])
            wlr = float(table[i + 1][0])
            irdr = float(table[i + 1][1])

            if irdl < 0 or irdr < 0:  # filter
                # print(str(wll) + '\t0.0')
                continue

            if weight_func == 'ery':
                from nldc_entity.ref_func import erythemal_action_spectrum as eryf
                weightl = eryf(wll)
                weightr = eryf(wlr)
            elif weight_func == 'vitd':
                from nldc_entity.ref_func import vitd_weight_func_interpolated as vitdf
                weightl = vitdf(wll)
                weightr = vitdf(wlr)
            elif weight_func == 'uv_hazard':
                from nldc_entity.ref_func import actinic_uv_weight_func as actuvf
                weightl = actuvf(wll)
                weightr = actuvf(wlr)
            else:
                weightl = 1
                weightr = 1

            if range_val1 <= wll < range_val2:
                try:
                    # calculate weighted integration
                    if alg == 'trapezoid':
                        e = 0.5 * (wlr - wll) * (irdl * weightl + irdr * weightr)
                    else:  # alg == 'rect'
                        # print(str(wll) + '\t' + str(irdl*weightl))
                        e = (wlr - wll) * (irdl * weightl)
                except TypeError:
                    print('exception!')
                    break

                broadband_ird += e
            else:
                pass

        return broadband_ird

    @staticmethod
    def get_specirrad_table(fname):
        # CAS파일(fname=FILExxxxx.ISD)의 분광(SPECtral IRRADinace) 데이터 테이블 반환
        # ex) [[wl, ird], ... , []]

        file = open(fname, 'rt', encoding='utf-8', errors='ignore')
        line = file.readline()
        table = []
        valid = False

        while line:
            if valid:
                try:
                    table.append(line.strip().split())
                except IndexError:
                    break
            if line.strip() == 'Data':
                valid = True
            line = file.readline()

        return table

    def get_attrib_fast(self, fname, attrib):
        # CAS파일(fname=FILExxxxx.ISD)의 조도 값을 float 단일 값으로 반환
        # select attrib
        category = '[Results]'
        key = ''

        if attrib == 'inttime':
            key = 'IntegrationTime [ms]'
        elif attrib == 'illum':
            key = 'Photometric [lx]'
        elif attrib == 'uva':
            key = 'UVA [W/m²]'
        elif attrib == 'uvb':
            key = 'UVB [W/m²]'
        elif attrib == 'uvc':
            key = 'UVC [W/m²]'
        elif attrib == 'vis':
            key = 'VIS [W/m²]'
        elif attrib == 'cct':
            key = 'CCT [K]'
        elif attrib == 'colorcoord_x':
            key = 'ColorCoordinates/x'
        elif attrib == 'colorcoord_y':
            key = 'ColorCoordinates/y'
        elif attrib == 'colorcoord_z':
            key = 'ColorCoordinates/z'
        elif attrib == 'colorcoord_u':
            key = 'ColorCoordinates/u'
        elif attrib == 'peakwl':
            key = 'PeakWavelength [nm]'
        elif attrib == 'cri':
            key = 'CRI'
        elif attrib == 'cdi':
            key = 'CDI'
        elif attrib == 'date':
            category = '[General Information]'
            key = 'Date'
        elif attrib == 'time':
            category = '[General Information]'
            key = 'Time'

        file = open(fname, 'rt', encoding='utf-8', errors='ignore')
        line = file.readline()
        valid = False
        value = 0.0

        while line:
            if valid:
                # print(line)
                try:
                    linesplit = line.split('=')
                    if linesplit[0] == key:
                        value = linesplit[1].strip()
                except IndexError as e:
                    break
                if line == '\n\r\n':
                    break
            if line.strip() == category:
                valid = True
            line = file.readline()

        return value

    def log_csv(self, rootdir):
        # .ISD파일들이 들어있는 디렉토리명을 루트 디렉토리로 적어줘야함
        # 생성될 csv 파일은 rootdir에 저장됨
        outputFileName = '_output_jake.csv'

        # 루트 디렉토리의 파일명리스트 가져오기
        filelist = self.search(rootdir)

        # csv 파일 출력 설정
        outfile = open(rootdir + '/' + outputFileName, 'w', encoding='utf-8', newline='')
        csv_writer = csv.writer(outfile)
        # csv 첫줄에 컬럼명 적어주기
        csv_writer.writerow(['time', 'illum', 'tuv', 'uva', 'uvb', 'euva', 'euvb', 'uvi'])

        # 각 파일별 데이터 추출하기
        for fname in filelist:
            datatable = self.get_specirrad_table(fname)
            hazard_uv = self.get_ird(datatable, 200, 400, weight_func='uv_hazard')
            uva = self.get_ird(datatable, 315, 400)
            uvb = self.get_ird(datatable, 280, 315)
            euva = self.get_ird(datatable, 315, 400, weight_func='ery')
            euvb = self.get_ird(datatable, 280, 315, weight_func='ery')
            uvi = 40 * self.get_ird(datatable, 280, 400, weight_func='ery')

            # filter
            # if euvb + euva == 0:
            #     ratio = 0
            # else:
            #     ratio = euvb / (euvb + euva)

            # ccx = get_result_attrib(fname, 'colorcoord_x')
            # ccy = get_result_attrib(fname, 'colorcoord_y')
            # ccz = get_result_attrib(fname, 'colorcoord_z')
            # ccu = get_result_attrib(fname, 'colorcoord_u')
            # cct = get_result_attrib(fname, 'cct')
            # cri = get_result_attrib(fname, 'cri')
            # ccdtemp = get_CCDTemp(fname)

            # if bbirrad != 0:
            #     swr = get_bbird(380, 480, datatable) / bbirrad
            #     narrow = get_bbird(446, 477, datatable) / bbirrad
            # else:
            #     swr = 0
            #     narrow = 0

            # 콘솔에 출력
            # print('time:', timestamp, ', euva:', euva, ', euvb:', euvb, ', ratio:', ratio, ', illum:', illum)

            # csv write
            csv_writer.writerow([hazard_uv, uva, uvb, euva, euvb, uvi])

        outfile.close()


if __name__ == '__main__':
    rootdir = 'D:/Desktop'
    outputFileName = 'Data.txt'

    flist = CasEntity.search(rootdir)
    outfile = open(rootdir + '/' + outputFileName, 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(outfile)

    csv_writer.writerow(['tuv', 'uva', 'uvb', 'euv', 'euva', 'euvb',
                         'uvi', 'duv', 'euva_ratio', 'euvb_ratio', 'hazard_uv'])

    for fname in flist:
        # print('>>' + fname)
        entity = CasEntity(fname)
        csv_writer.writerow(CasEntity.get_dict_to_list(entity.get_dict('uv'), kv=False))

    outfile.close()
