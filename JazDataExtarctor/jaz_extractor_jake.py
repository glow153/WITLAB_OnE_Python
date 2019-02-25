import os
import csv
import ref_func as rf


def get_file_list(dirname):
    # dirname 디렉토리 내의 모든 파일과 디렉토리 이름을 리스트로 반환

    filelist = []
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        filelist.append(full_filename)
    return filelist


def get_time(fname):
    # Jaz파일(fname=spxxxxx.txt)의 시간 값을 string 형태로 반환
    # ex. Fri Apr 20 10:51:04 KST 2018

    file = open(fname, 'rt', encoding='utf-8', errors='ignore')
    line = file.readline()
    valid = False
    infotime = ''

    while line:
        if valid:
            try:
                linesplit = line.split(': ')
                if linesplit[0] == 'Date':
                    infotime = linesplit[1].strip()
            except IndexError:
                break
        if line.strip() == '++++++++++++++++++++++++++++++++++++':
            valid = True
        line = file.readline()

    return infotime


def get_specirrad_table(fname):
    # Jaz파일(fname=spxxxxx.txt)의 분광(SPECtral IRRADinace) 데이터 테이블 반환
    # ex) [[wl, ird], ... , []]

    file = open(fname, 'rt', encoding='utf-8', errors='ignore')
    table = []

    line = file.readline()
    if line == 'SpectralSuite Data File':
        valid = True
    else:
        valid = False

    while line:
        if valid:

            try:
                table.append(line.strip().split())
            except IndexError:
                break
        if line.strip() == '>>>>>Begin Processed Spectral Data<<<<<':
            valid = True
        line = file.readline()

    return table


def get_ird(table, range_val1, range_val2, weight_func='none', alg='rect'):
    # 분광 데이터 테이블로부터 특정 범위에 대한 광파장 복사량(broadband irradiance)을
    # float 단일값으로 반환 (광파장복사량 == 적산 값)
    # range_val1, range_val2 : 적분구간 시작, 끝 값
    # table : get_dict_to_list()로부터 생성된 분광 데이터 테이블(list)
    # weight_func : 가중함수 선택, 홍반가중함수('ery'), 비타민 d 가중함수('vitd'), 없음('none')
    # alg : 적분 알고리즘 선택, 기본값('rect')은 직사각형 공식, 'trapezoid' 로 설정하면 사다리꼴 공식 적용

    broadband_ird = 0

    for i in range(len(table) - 2):
        wll = float(table[i][0])
        irdl = float(table[i][1]) / 100
        wlr = float(table[i + 1][0])
        irdr = float(table[i + 1][1]) / 100

        if irdl < 0 or irdr < 0:  # filter
            # print(str(wll) + '\t0.0')
            continue

        if weight_func == 'ery':
            from ref_func import erythemal_action_spectrum as eryf
            weightl = eryf(wll)
            weightr = eryf(wlr)
        elif weight_func == 'vitd':
            from ref_func import vitd_weight_func as vitdf
            weightl = vitdf(wll)
            weightr = vitdf(wlr)
        elif weight_func == 'uv_hazard':
            from ref_func import uv_hazard_weight_func as uvhzf
            weightl = uvhzf(wll)
            weightr = uvhzf(wlr)
        else:
            weightl = 1
            weightr = 1

        if range_val1 <= int(float(table[i][0])) < range_val2:
            try:
                # calculate weighted integration
                if alg == 'trapezoid':
                    e = 0.5 * (wlr - wll) * (irdl * weightl + irdr * weightr)
                else:  # alg == 'rect'
                    # print(str(wll) + '\t' + str(irdl*weightl))
                    e = (wlr - wll) * irdl * weightl
            except TypeError:
                print('exception!')
                break

            broadband_ird += e
        else:
            pass

    return broadband_ird


# def get_bbird(range_val1, range_val2, table, alg='rect'):
#     # 분광 데이터 테이블로부터 특정 범위에 대한 광파장 복사량(BroadBandIRaDiance)을
#     # float 단일값으로 반환 (광파장복사량 == 적산 값)
#     # range_val1, range_val2 : 적분구간 시작, 끝 값
#     # table : get_specirrad()로부터 생성된 분광 데이터 테이블
#     # alg : 적분 알고리즘 선택, 'rect' : 직사각형 공식(기본값), 'trapezoid' : 사다리꼴 공식
#
#     bbirad = 0
#
#     for i in range(len(table)-1):
#         if alg == 'trapezoid':
#             if range_val1 <= int(float(table[i][0])) < range_val2:
#                 wl1 = float(table[i][0])
#                 wl2 = float(table[i + 1][0])
#                 # ird1 = float(table[i][1])
#                 ird1 = float(table[i][1]) / 100  # uW/cm^2 -> W/m^2
#                 ird2 = float(table[i + 1][1]) / 100
#                 if ird1 < 0:  # filter
#                     ird1 = 0
#                 if ird2 < 0:  # filter
#                     ird2 = 0
#                 try:
#                     e = 0.5 * (wl2 - wl1) * (ird1 + ird2)
#                     bbirad += e
#                 except TypeError:
#                     break
#         else:
#             if range_val1 <= int(float(table[i][0])) < range_val2:
#                 wll = float(table[i-1][0])
#                 wlr = float(table[i][0])
#                 # ird = float(table[i][1])
#                 ird = float(table[i][1]) / 100  # uW/cm^2 -> W/m^2
#                 if ird < 0:  # filter
#                     ird = 0
#                 try:
#                     e = (wlr - wll) * ird
#                     bbirad += e
#                 except TypeError:
#                     break
#     return bbirad
#

# def get_euv(range_val1, range_val2, table, alg='rect'):
#     # 분광 데이터 테이블로부터 특정 범위에 대한 홍반자외선복사량(EUV)을 float 단일값으로 반환
#     # range_val1, range_val2 : 적분구간 시작, 끝 값
#     # table : 분광 데이터 테이블
#     # alg : 적분 알고리즘 선택
#
#     euv = 0
#
#     for i in range(len(table)-1):
#         # print(table[i][0] + " : " + table[i][1])
#         if alg == 'trapezoid':
#             if range_val1 <= int(float(table[i][0])) < range_val2:
#                 wl1 = float(table[i][0])
#                 wl2 = float(table[i + 1][0])
#                 ird1 = float(table[i][1]) / 100
#                 ird2 = float(table[i + 1][1]) / 100
#                 if ird1 < 0:
#                     ird1 = 0
#                 if ird2 < 0:
#                     ird2 = 0
#                 try:
#                     e = 0.5 * (wl2 - wl1) * (
#                             ird1 * rf.erythemal_action_spectrum(wl1) + ird2 * rf.erythemal_action_spectrum(wl2))
#                     # print(e)
#                     euv += e
#                 except TypeError:
#                     break
#         else:   # alg == 'rect'
#             if range_val1 <= int(float(table[i][0])) < range_val2:
#                 wll = float(table[i - 1][0])
#                 wlr = float(table[i][0])
#                 ird = float(table[i][1]) / 100
#                 if ird < 0:
#                     ird = 0
#
#                 try:
#                     e = (wlr - wll) * ird * rf.erythemal_action_spectrum(wlr)
#                     # print(e)
#                     euv += e
#                 except TypeError:
#                     break
#     return euv


def log_csv(rootdir):
    # .ISD파일들이 들어있는 디렉토리명을 루트 디렉토리로 적어줘야함
    # 생성될 csv 파일은 rootdir에 저장됨
    outputFileName = '_output_jake.csv'

    # 루트 디렉토리의 파일명리스트 가져오기
    filelist = get_file_list(rootdir)

    # csv 파일 출력 설정
    outfile = open(rootdir + '/' + outputFileName, 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(outfile)
    # csv 첫줄에 컬럼명 적어주기
    csv_writer.writerow(['fname', 'uva', 'uvb', 'euva', 'euvb', 'uvi', 'auv', 'nuv'])

    # 각 파일별 데이터 추출하기
    for fname in filelist:
        print(fname)
        datatable = get_specirrad_table(fname)
        print(datatable)
        # time = get_time(fname)

        uva = get_ird(datatable, 315, 400)
        uvb = get_ird(datatable, 280, 315)
        euva = get_ird(datatable, 315, 400, 'ery')
        euvb = get_ird(datatable, 280, 315, 'ery')
        uvi = 40 * get_ird(datatable, 280, 400, 'ery')
        auv = get_ird(datatable, 280, 400, 'uv_hazard')
        nuv = get_ird(datatable, 315, 400)

        # csv write
        csv_writer.writerow([fname, uva, uvb, euva, euvb, uvi, auv, nuv])

    outfile.close()


def log_csv_mergedtable(fname):
    outputFileName = '_output_jake.csv'

    # csv 파일 출력 설정
    outfile = open('C:/Users/Witlab/Desktop/' + outputFileName, 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(outfile)
    # csv 첫줄에 컬럼명 적어주기
    csv_writer.writerow(['swr', 'narrow'])

    # 데이터 추출하기
    infile = open(fname, 'rt', encoding='utf-8', errors='ignore')
    column = infile.readline()
    col_count = len(column.split(',')) - 1
    datarow = infile.readline()
    spectrals = []

    for i in range(col_count):
        spectrals.append([])

    while datarow:
        datarow = infile.readline().split(',')
        print('datarow length =', len(datarow))
        if len(datarow) < col_count:
            break
        for i in range(col_count):
            print([datarow[0], datarow[i+1]])
            spectrals[i].append([float(datarow[0].strip()),
                                 float(datarow[i+1].strip())
                                 ])

    # print(spectrals)
    for datatable in spectrals:
        # uva = get_bbird(315, 400, datatable)
        # uvb = get_bbird(280, 315, datatable)
        # euva = get_euv(315, 400, datatable)
        # euvb = get_euv(280, 315, datatable)
        # uvi = 40 * get_euv(280, 400, datatable)

        # filter
        # if euvb + euva == 0:
        #     ratio = 0
        # else:
        #     ratio = euvb / (euvb + euva)

        bb = get_bbird(380, 780, datatable)
        bbswr = get_bbird(380, 480, datatable)
        bbnarrow = get_bbird(446, 477, datatable)

        if bb == 0:
            swr = 0
            narrow = 0
        else:
            swr = bbswr / bb
            narrow = bbnarrow / bb

        # csv write
        print('swr, narrow : ', [swr, narrow])
        csv_writer.writerow([swr, narrow])

    outfile.close()
    infile.close()
