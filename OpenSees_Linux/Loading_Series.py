# -*- coding: utf-8 -*
def Loading_Series(Load_Path, Col_Rot, Col_Twr, Col_Fod, Aero_Twr):
    Data = []
    with open(Load_Path, 'r', encoding='UTF-8') as Load_File:
        for line in Load_File:
            Data.append(line.rstrip())
    Data = Data[8:]

    Time = []
    Dic_Twr = {}
    Dic_Rot = {}
    Dic_Fod = {}
    Ht = Aero_Twr.Ht
    for i in range(len(Col_Rot)):
        Dic_Rot[i] = []
    for i in range(len(Col_Twr)):
        Dic_Twr[i] = []
    for i in range(len(Col_Fod)):
        Dic_Fod[i] = []

    for row in Data:
        lines = row.split('\t')
        templine = []
        for linedata in lines:
            rd = float(linedata)
            templine.append(rd)
        Time.append(templine[0])
        for j in range(len(Col_Rot)):
            Dic_Rot[j].append(templine[Col_Rot[j]])
        for j in range(len(Col_Twr)):
            Dic_Twr[j].append(templine[Col_Twr[j]]*Ht[j])
        for j in range(len(Col_Fod)):
            Dic_Fod[j].append(templine[Col_Fod[j]])
    Load_File.close()

    return Time, Dic_Rot, Dic_Twr, Dic_Fod
