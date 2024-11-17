 # -*- coding: utf-8 -*
import os
import numpy as np
from IM_Analysis import IM_Analysis
from joblib import Parallel, delayed
# Main settings and main paths
Num_Records = 30  # 每个IM相应的工况数
NOP = 60  # 调用核数
File_OpenFAST = '5MW_Tripod.fst'  # .fst文件名
Name = File_OpenFAST.split('.')[0]
Path_OpenFAST = '/public4/home/sc57135/IEA_15MW_Monopile/OpenFAST_IEA_15MW_Monopile'  # .fst及.exe路径
Destination = '/public4/home/sc57135/IEA_15MW_Monopile/Result_IEA_15MW_Monopile/Result_03-25mps_NOM'  # .out和.sum结果存放目录
## Operation mode
Operation_Condition = ['Operation', 'Park', 'Idle', 'Emergency Shutdown']
Mode = 0
WindSpeed = [[str(x) for x in np.arange(3, 26, 1)],
             [str(x) for x in np.arange(26, 120, 4)],
             [str(x) for x in np.arange(26, 120, 4)],
             [str(x) for x in np.arange(26, 100, 4)]]
Num_IM = [len(x) for x in WindSpeed]
Length_IM = Num_IM[Mode]
WindType = ['NTM', '1ETM', '1ETM', '1ETM']
WaveHs = [[str(0.0002491*x**3-0.009742*x**2+0.3361*x-1.092+0.17) for x in [int(y) for y in WindSpeed[0]]],
          ['5.439', '6.949', '8.864', '11.281', '14.295'] + ['18.001']*(Num_IM[1]-5),
          ['5.439', '6.949', '8.864', '11.281', '14.295'] + ['18.001']*(Num_IM[2]-5),
          ['5.439', '6.949', '8.864', '11.281', '14.295'] + ['18.001']*(Num_IM[3]-5)]
WaveTp = [[str(0.0003416*x**3-0.02636*x**2+0.9053*x-0.3805) for x in [int(y) for y in WindSpeed[0]]],
          ['11.342', '12.278', '13.354', '14.701', '16.452'] + ['18.736']*(Num_IM[1]-5),
          ['11.342', '12.278', '13.354', '14.701', '16.452'] + ['18.736']*(Num_IM[2]-5),
          ['11.342', '12.278', '13.354', '14.701', '16.452'] + ['18.736']*(Num_IM[3]-5)]
BlPitch = [['0']*9 + [str((1.168*x**2-16.92*x+41.15)/(x-10.24)) for x in np.arange(12, 26, 1)],
           ['90']*Num_IM[1],
           ['90']*Num_IM[2],
           ['23.47']*Num_IM[3]]
RotSpeed = ['12.1', '0', '12.1', '12.1']
TPCOn = ['0', '9999.9', '9999.9', '0']
TPitManS = ['9999.9', '0', '9999.9', '0']
PitManRat = ['2', '2', '2', '8']
BlPitchF = ['0', '90', '90', '90']
TimGenOn = ['0', '9999.9', '0', '0']
TimGenOf = ['9999.9', '0', '9999.9', '0']
# Load cases
# TurbSim
File_TurbSim = 'TurbSim.inp'
Path_TurbSim = Path_OpenFAST + '/InflowData'
TurbSim_Str = ['URef', 'TurbModel', 'IECstandard', 'IECturbc', 'IEC_WindType', 'ETMc', 'WindProfileType', 'PLExp', 'Z0']
TurbSim_Value = ['']*len(TurbSim_Str)
TurbSim_Value[0] = WindSpeed[Mode]
TurbSim_Value[1] = ['IECKAI']*Length_IM
TurbSim_Value[2] = ['3']*Length_IM
TurbSim_Value[3] = ['B']*Length_IM
TurbSim_Value[4] = [WindType[Mode]]*Length_IM
TurbSim_Value[5] = ['default']*Length_IM
TurbSim_Value[6] = ['PL']*Length_IM
TurbSim_Value[7] = ['default']*Length_IM
TurbSim_Value[8] = ['default']*Length_IM
# HydroDyn
File_HydroDyn = '{}_HydroDyn.dat'.format(Name)
Path_HydroDyn = Path_OpenFAST
HydroDyn_Str = ['WaveHs', 'WaveTp']
HydroDyn_Value = ['']*len(HydroDyn_Str)
HydroDyn_Value[0] = WaveHs[Mode]
HydroDyn_Value[1] = WaveTp[Mode]
# Operation mode
# ElastoDyn
File_ElastoDyn = '{}_ElastoDyn.dat'.format(Name)
Path_ElastoDyn = Path_OpenFAST
ElastoDyn_Str = ['BlPitch(1)', 'BlPitch(2)', 'BlPitch(3)', 'RotSpeed']
ElastoDyn_Value = ['']*len(ElastoDyn_Str)
ElastoDyn_Value[0] = BlPitch[Mode]
ElastoDyn_Value[1] = ElastoDyn_Value[0]
ElastoDyn_Value[2] = ElastoDyn_Value[0]
ElastoDyn_Value[3] = [RotSpeed[Mode]]*Length_IM
# ServoDyn
File_ServoDyn = '{}_ServoDyn.dat'.format(Name)
Path_ServoDyn = Path_OpenFAST
ServoDyn_Str = ['TPitManS(1)', 'TPitManS(2)', 'TPitManS(3)', 'PitManRat(1)', 'PitManRat(2)', 'PitManRat(3)', 'BlPitchF(1)', 'BlPitchF(2)', 'BlPitchF(3)', 'TimGenOn', 'TimGenOf', 'TPCOn']
ServoDyn_Value = ['']*len(ServoDyn_Str)
ServoDyn_Value[0] = [TPitManS[Mode]]*Length_IM  # 9999.9 for running mode and 0 for park mode
ServoDyn_Value[1] = ServoDyn_Value[0]
ServoDyn_Value[2] = ServoDyn_Value[0]
ServoDyn_Value[3] = [PitManRat[Mode]]*Length_IM  # 2 for running mode and 8 for ES mode
ServoDyn_Value[4] = ServoDyn_Value[3]
ServoDyn_Value[5] = ServoDyn_Value[3]
ServoDyn_Value[6] = [BlPitchF[Mode]]*Length_IM  # 0 for running mode and 90 for park mode
ServoDyn_Value[7] = ServoDyn_Value[6]
ServoDyn_Value[8] = ServoDyn_Value[6]
ServoDyn_Value[9] = [TimGenOn[Mode]]*Length_IM  # 0 for running mode and 9999.9 for park mode
ServoDyn_Value[10] = [TimGenOf[Mode]]*Length_IM  # 9999.9 for running mode and 0 for park mode
ServoDyn_Value[11] = [TPCOn[Mode]]*Length_IM
# InflowWind
File_InflowWind = '{}_InflowWind.dat'.format(Name)
Path_InflowWind = Path_OpenFAST
# Parallel
os.chdir(Path_OpenFAST)
for IM_i in range(Length_IM):
    FilePath = Destination + '/{}mps'.format(str(TurbSim_Value[0][IM_i]))
    if not os.path.isdir(FilePath):
        os.mkdir(FilePath)
    Parallel(n_jobs=NOP)(delayed(IM_Analysis)(num+1, File_OpenFAST, Name, Path_OpenFAST, Destination,
                                              File_TurbSim, Path_TurbSim, TurbSim_Str, [TV[IM_i] for TV in TurbSim_Value],
                                              File_HydroDyn, Path_HydroDyn, HydroDyn_Str, [HV[IM_i] for HV in HydroDyn_Value],
                                              File_ElastoDyn, Path_ElastoDyn, ElastoDyn_Str, [EV[IM_i] for EV in ElastoDyn_Value],
                                              File_ServoDyn, Path_ServoDyn, ServoDyn_Str, [SV[IM_i] for SV in ServoDyn_Value],
                                              File_InflowWind, Path_InflowWind)
                         for num in range(Num_Records))
