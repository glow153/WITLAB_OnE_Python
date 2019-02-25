import csv


path = '/home/witlab/dw/pm/pm_cheonan.csv'

infile = open(path, 'r', encoding='utf-8', newline='')

line = infile.readline()
lsData = []
lsData_rev = []

print('>> old file content:')
while line.strip():
    print(line.strip())
    lsData.append(line.strip())
    line = infile.readline()

for i in reversed(range(len(lsData))):
    lsData_rev.append(lsData[i])

print('>> new file content:')
outfile = open(path.split('.')[0] + '-new.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(outfile)
for row in lsData_rev:
    print(row)
    csv_writer.writerow(row.split(','))

outfile.close()

