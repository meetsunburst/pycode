intput_file = r"C:\Users\dragon\Desktop\WT-Spectrum.txt"
# inputFile = r"C:\Users\dragon\Desktop\JW-Spectrum.txt"
output_file = r"C:\Users\dragon\Desktop\res.csv"

with open(file=intput_file, mode='r', encoding='utf-8') as file_in:
    with open(file=output_file, mode='w', encoding='utf-8') as file_out:
        line_count = 0
        line = file_in.readline()
        dic = {}
        level1 = None
        level2 = None
        while line:
            if (line_count % 2 == 0):
                level1 = line.strip()
            else:
                level2 = line.strip()
                if((level1,level2) in dic):
                    dic[(level1, level2)]+=1
                else:
                    dic[(level1, level2)] = 1

            line_count += 1
            line = file_out.readline()

        for i in dic:
            file_out.write(i[0] + ',' + i[1] + ',' + str(dic[i]) + "\n")
