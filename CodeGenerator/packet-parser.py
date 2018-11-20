import csv

def normalform(line):
    ret = []
    for s in line.split(','):
        value = int(s)
        if value < 0:
            value += 256
        ret.append(value)
    if sum(ret) > 255:
        for idx in range(4):
            if ret[3-idx] != 0:
                ret[3 - idx] -= 1
                break
    return ret


rootdir = 'D:/Desktop/jgc'
# rootdir = '.'
rawfile = open(rootdir + '/control_index.csv', 'r', encoding='utf-8', newline='')

output_raw = []

head = '\t{(byte)0x01,(byte)0x02,'
tail = '},'
print('byte[][] packet_table = { ')
while True:
    line = rawfile.readline()
    if not line:
        break

    lpacket = normalform(line)

    output = head
    for e in lpacket:
        output += '(byte)' + str(e) + ','
    output = output[:-1] + tail

    print(output)
    output_raw.append(lpacket)

print('};')
rawfile.close()

outfile = open(rootdir + '/control_index_e.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(outfile)
for i in output_raw:
    csv_writer.writerow(i)
outfile.close()
