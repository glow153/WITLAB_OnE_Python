rootdir = 'D:/Desktop/jgc'
rawfile = open(rootdir + '/ratio_table.csv', 'r', encoding='utf-8', newline='')
lsPacket = []

print('float[][] ratio_table = { ')
while True:
    line = rawfile.readline()
    if not line:
        break
    output = '\t{'
    for e in line.split(','):
        output += str(round(float(e.strip()), 3)) + ','
    output += '},'

    print(output)

print('};')
rawfile.close()
