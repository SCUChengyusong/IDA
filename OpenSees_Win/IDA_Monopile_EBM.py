# -*- coding: utf-8 -*
import os
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from Model_Monopile import Monopile_Build

NOP = 64
File_Path = '/work/home/aco7liy2y0/CYS/Fragility_Failed/Code/'
File_Name = 'Property_NREL5MWMonopile.xlsx'
Sheet_Name = ['Nodes', 'Elements', 'Sections', 'AeroDyn']
Nodes = pd.read_excel(File_Path + File_Name, sheet_name=Sheet_Name[0], header=0)
Elements = pd.read_excel(File_Path + File_Name, sheet_name=Sheet_Name[1], header=0)
Sections = pd.read_excel(File_Path + File_Name, sheet_name=Sheet_Name[2], header=0)
Aero_Twr = pd.read_excel(File_Path + File_Name, sheet_name=Sheet_Name[3], header=0)
Load_Path = '/work/home/aco7liy2y0/CYS/Fragility_Failed/IDA_Result/EBM/'
Re_Path = '/work/home/aco7liy2y0/CYS/Fragility_Failed/IDA_Result/EBM_P/'

WindSpeed = np.arange(3, 26, 1)
Num_IM = len(WindSpeed)
Samples = []
with open((File_Path + 'Samples.txt'), 'r', encoding='UTF-8') as File:
    for line in File:
        Samples.append(float(line.rstrip()))
File.close()
Num_S = 50
Num_Records = 30

for ii in range(Num_S):
    MYS = Samples[ii]*1E6
    Path1 = (Re_Path + 'Stress_' + str(ii+1))
    if not os.path.isdir(Path1):
        os.mkdir(Path1)
    for jj in range(Num_IM):
        WS = WindSpeed[jj]
        Path2 = (Re_Path + 'Stress_' + str(ii+1) + '/' + str(WS) + 'mps')
        if not os.path.isdir(Path2):
            os.mkdir(Path2)
        Result_Path = (Re_Path + 'Stress_' + str(ii+1) + '/' + str(WS) + 'mps/')
        Parallel(n_jobs=NOP)(delayed(Monopile_Build)(Nodes, Elements, Sections, Aero_Twr, Load_Path, Result_Path, MYS, kk+1, WS) for kk in range(Num_Records))
