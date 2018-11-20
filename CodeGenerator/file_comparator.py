file1 = open('C:/Users/Witlab/Desktop/control-table-total_normalform.csv', 'r', encoding='utf-8', newline='')
file2 = open('C:/Users/Witlab/Desktop/control-table-total_2.csv', 'r', encoding='utf-8', newline='')

line1 = file1.readline()
line2 = file2.readline()

while line1 and line2:
    if line1 != line2:
        print(line1, line2)
    line1 = file1.readline()
    line2 = file2.readline()

