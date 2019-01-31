import os


def append_header(dirname, header):
    fnamelist = os.listdir(dirname)
    for fname in fnamelist:
        os.rename(dirname + '/' + fname, dirname + '/' + header + fname)


def mod(dirname):
    fnamelist = os.listdir(dirname)
    for fname in fnamelist:
        os.rename(dirname + '/' + fname, dirname + '/FILE0' + fname[5:])


if __name__ == "__main__":
    mod('D:/_nldw/all/20180425_1')

