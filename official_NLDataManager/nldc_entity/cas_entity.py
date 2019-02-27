import datetime
import os


class CasEntity:
    __measurement_conditions = {}
    __results = {}
    __general_information = {}
    __data = {}
    __uv = {}
    valid = None
    objDatetime = None

    def __init__(self, fname):
        isdfile = open(fname, 'rt', encoding='utf-8', errors='ignore')
        self.valid = self.__map_data(isdfile)
        isdfile.close()

        if self.valid:
            self.__set_additional_data(alg='trapezoid')
            self.__set_uv_dict()
            self.objDatetime = datetime.datetime.strptime(
                self.__general_information['Date'] + ' ' + self.__general_information['Time'], '%m/%d/%Y %I:%M:%S %p')

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

    def __set_additional_data(self, alg='rect'):
        bird_vis = self.get_ird(380, 780, alg=alg)
        bird_sw = self.get_ird(380, 480, alg=alg)
        bird_mw = self.get_ird(480, 560, alg=alg)
        bird_lw = self.get_ird(560, 780, alg=alg)
        bird_narrow = self.get_ird(446, 477, alg=alg)

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

    def __set_uv_dict(self):
        self.__uv['tuv'] = self.get_ird(280, 400)
        self.__uv['uva'] = self.get_ird(315, 400)
        self.__uv['uvb'] = self.get_ird(280, 315)
        self.__uv['euv'] = self.get_ird(280, 400, weight_func='ery')
        self.__uv['euva'] = self.get_ird(315, 400, weight_func='ery')
        self.__uv['euvb'] = self.get_ird(280, 315, weight_func='ery')
        self.__uv['uvi'] = self.__uv['euv'] * 40
        self.__uv['duv'] = self.get_ird(280, 400, weight_func='vitd')

        if self.__uv['euv'] == 0:
            self.__uv['euva_ratio'] = 0
            self.__uv['euvb_ratio'] = 0
        else:
            self.__uv['euva_ratio'] = self.__uv['euva'] / self.__uv['euv']
            self.__uv['euvb_ratio'] = self.__uv['euvb'] / self.__uv['euv']

        self.__uv['auv'] = self.get_ird(200, 400, weight_func='actinic_uv', alg='trapezoid')

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
    def search(dirname):  # dirname 디렉토리 내의 모든 파일과 디렉토리 이름을 리스트로 반환함
        filelist = []
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            filelist.append(full_filename)
        return filelist

    def get_ird(self, range_val_left, range_val_right, weight_func='none', alg='rect'):
        ird = 0
        if self.__data:
            wls = list(self.__data.keys())

            # for debug
            # print(wls)

            for i in range(len(wls) - 2):
                wll = float(wls[i])
                wlr = float(wls[i+1])
                irdl = self.__data[wll]
                irdr = self.__data[wlr]

                if irdl < 0 or irdr < 0:  # filter noise (negative value)
                    continue

                if weight_func == 'ery':
                    from nldc_entity.ref_func import erythemal_action_spectrum as eryf
                    weightl = eryf(wll)
                    weightr = eryf(wlr)
                elif weight_func == 'vitd':
                    from nldc_entity.ref_func import vitd_weight_func_interpolated as vitdf
                    weightl = vitdf(wll)
                    weightr = vitdf(wlr)
                elif weight_func == 'actinic_uv':
                    from nldc_entity.ref_func import actinic_uv_weight_func as actuvf
                    weightl = actuvf(wll)
                    weightr = actuvf(wlr)
                else:
                    weightl = 1
                    weightr = 1

                if range_val_left <= wll < range_val_right:
                    try:
                        # calculate weighted integration
                        if alg == 'trapezoid':
                            e = 0.5 * (wlr - wll) * (irdl * weightl + irdr * weightr)
                        else:  # alg == 'rect'
                            # print(str(wll) + '\t' + str(irdl*weightl))
                            e = (wlr - wll) * (irdl * weightl)
                    except TypeError:
                        print('get_ird(): spectral irradiance value exception!')
                        break

                    ird += e
                else:
                    pass

            return ird
        else:
            return


if __name__ == '__main__':
    rootdir = 'D:/Desktop/확장곰국용/20181003'
    flist = CasEntity.search(rootdir)

    for fname in flist:
        # print('>>' + fname)
        entity = CasEntity(fname)
        a = entity.get_ird(200, 800)
        print(a)


