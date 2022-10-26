inputFileName = r'D:\double-15hz.txt'
outPutFileName = r'D:\double.blk'

theDate = 'Tue Jun 27 11:48:26 2017'
Max = '14.22'
Min = '0.41'
Dimension = 'Force'

Frequency = '10.00'
Count = '1.000'
Shape = 'Sine'

with open(file=inputFileName, mode='r', encoding='utf-8') as fIn:
    with open(file=outPutFileName, mode='w', encoding='utf-8') as fOut:
        fOut.write('FileType=Block-Arbitrary\n')
        fOut.write('Date=%s\n' % theDate)
        fOut.write('\n')
        fOut.write('Channel(1)=Channel 1\n')
        fOut.write('Max=%s KN\n' % Max)
        fOut.write('Min=%s KN\n' % Min)
        fOut.write('Dimension= %s\n' % Dimension)
        fOut.write('\n')
        fOut.write('%-17s%-16s%-16s%-16s%-16s\n' % ('Frequency', 'Count', 'Shape', 'Level1', 'Level2'))
        fOut.write('%-17s%-16s%-16s%-16s%-16s\n' % ('Hz', 'cycles', 'NA', 'kN', 'kN'))
        level1 = None
        level2 = None
        line = fIn.readline()
        lineCounter = 0
        while line:
            if lineCounter % 2 == 0:
                level1 = line.strip()
            else:
                level2 = line.strip()
                fOut.write('%-17s%-16s%-16s%-16s%-16s\n' % (Frequency, Count, Shape, level1, level2))
            line = fIn.readline()
            lineCounter += 1
        fOut.write('\n')
        fOut.write('\n')
        fOut.write('\n')
        fOut.write('\n')
