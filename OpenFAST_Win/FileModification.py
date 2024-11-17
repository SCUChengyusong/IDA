def FM(FileName, FilePath, Value, String, WindSpeed, num):
    count = 0
    File = []
    InputFile = open(FilePath + '/{}'.format(FileName), encoding='UTF-8')
    for line in InputFile:
        File.append(line.rstrip())
        ForeStr = line.split('-')
        for i in range(len(String)):
            if String[i] in ForeStr[0]:
                File[count] = Value[i] + ' '*5 + String[i]
        count += 1
    InputFile.close()
    with open(FilePath + '/{}mps_{}_{}'.format(WindSpeed, num, FileName), 'w') as file:
        file.write('\n'.join(File))
    file.close()
