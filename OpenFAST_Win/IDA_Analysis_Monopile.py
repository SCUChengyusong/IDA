 # -*- coding: utf-8 -*
import os
import numpy as np
from IM_Analysis import IM_Analysis
from joblib import Parallel, delayed
# Main settings and main paths
Num_Records = 30  # 每个IM相应的工况数
NOP = 8  # 调用核数
File_OpenFAST = '5MW_Monopile.fst'  # .fst文件名
Name = File_OpenFAST.split('.')[0]
Path_OpenFAST = 'E:/Fragility analysis/Damaged components/OpenFAST_Monopile'  # .fst及.exe路径
OpenFAST_exe = 'openfast_x64.exe'  # .exe名称
Destination = 'E:/Fragility analysis/Damaged components/IDA_Result/Intact/ESM2'  # .out和.sum结果存放目录
## Operation mode
Operation_Condition = ['Normal operating', 'Parked_intact', 'Emergent pitching', 'Idling', 'Parked_failed', 'Emergent HHS braking']
Mode = 0
WindSpeed = [str(x) for x in np.arange(3, 26, 1)]
Num_IM = len(WindSpeed)
BlPitch = [['0']*9 + [str((1.168*x**2-16.92*x+41.15)/(x-10.24)) for x in np.arange(12, 26, 1)],
           ['90']*Num_IM,
           ['23.47']*Num_IM,
           ['0']*Num_IM,
           ['0']*Num_IM,
           ['0']*Num_IM]
RotSpeed = ['12.1', '0', '12.1', '12.1', '0', '12.1']
TPCOn = ['0', '9999.9', '0', '9999.9', '9999.9', '9999.9']
TPitManS = ['9999.9', '0', '0', '9999.9', '9999.9', '9999.9']
PitManRat = ['2', '2', '8', '2', '2', '2']
BlPitchF = ['0', '90', '90', '0', '0', '0']
TimGenOn = ['0', '9999.9', '0', '0', '9999.9', '0']
TimGenOf = ['9999.9', '0', '150', '9999.9', '0', '0']
HSSBrMode = ['0', '0', '0', '0', '1', '1']
THSSBrDp = ['9999.9', '9999.9', '9999.9', '9999.9', '0', '0']

# Load cases
# TurbSim
File_TurbSim = 'TurbSim.inp'
Path_TurbSim = Path_OpenFAST + '/InflowData'
TurbSim_exe = 'TurbSim_x64.exe'
TurbSim_Str = ['URef', 'TurbModel', 'IECstandard', 'IECturbc', 'IEC_WindType', 'ETMc', 'WindProfileType', 'PLExp', 'Z0']
TurbSim_Value = ['']*len(TurbSim_Str)
TurbSim_Value[0] = WindSpeed
TurbSim_Value[1] = ['IECKAI']*Num_IM
TurbSim_Value[2] = ['3']*Num_IM
TurbSim_Value[3] = ['B']*Num_IM
TurbSim_Value[4] = ['NTM']*Num_IM
TurbSim_Value[5] = ['default']*Num_IM
TurbSim_Value[6] = ['PL']*Num_IM
TurbSim_Value[7] = ['default']*Num_IM
TurbSim_Value[8] = ['default']*Num_IM
# HydroDyn
File_HydroDyn = '{}_HydroDyn.dat'.format(Name)
Path_HydroDyn = Path_OpenFAST
HydroDyn_Str = ['WaveHs', 'WaveTp']
HydroDyn_Value = ['']*len(HydroDyn_Str)
HydroDyn_Value[0] = [str(-0.0005746*x**3+0.02619*x**2-0.08787*x+0.1258) for x in [int(y) for y in WindSpeed]]
HydroDyn_Value[1] = [str(-0.0002769*x**3-0.0001972*x**2+0.6065*x+0.4472) for x in [int(y) for y in WindSpeed]]
# Operation mode
# ElastoDyn
File_ElastoDyn = '{}_ElastoDyn.dat'.format(Name)
Path_ElastoDyn = Path_OpenFAST
ElastoDyn_Str = ['BlPitch(1)', 'BlPitch(2)', 'BlPitch(3)', 'RotSpeed']
ElastoDyn_Value = ['']*len(ElastoDyn_Str)
ElastoDyn_Value[0] = BlPitch[Mode]
ElastoDyn_Value[1] = ElastoDyn_Value[0]
ElastoDyn_Value[2] = ElastoDyn_Value[0]
ElastoDyn_Value[3] = [RotSpeed[Mode]]*Num_IM
# ServoDyn
File_ServoDyn = '{}_ServoDyn.dat'.format(Name)
Path_ServoDyn = Path_OpenFAST
ServoDyn_Str = ['TPitManS(1)', 'TPitManS(2)', 'TPitManS(3)', 'PitManRat(1)', 'PitManRat(2)', 'PitManRat(3)', 'BlPitchF(1)', 'BlPitchF(2)', 'BlPitchF(3)', 'TimGenOn', 'TimGenOf', 'TPCOn', 'HSSBrMode', 'THSSBrDp']
ServoDyn_Value = ['']*len(ServoDyn_Str)
ServoDyn_Value[0] = [TPitManS[Mode]]*Num_IM  # 9999.9 for running mode and 0 for park mode
ServoDyn_Value[1] = ServoDyn_Value[0]
ServoDyn_Value[2] = ServoDyn_Value[0]
ServoDyn_Value[3] = [PitManRat[Mode]]*Num_IM  # 2 for running mode and 8 for ES mode
ServoDyn_Value[4] = ServoDyn_Value[3]
ServoDyn_Value[5] = ServoDyn_Value[3]
ServoDyn_Value[6] = [BlPitchF[Mode]]*Num_IM  # 0 for running mode and 90 for park mode
ServoDyn_Value[7] = ServoDyn_Value[6]
ServoDyn_Value[8] = ServoDyn_Value[6]
ServoDyn_Value[9] = [TimGenOn[Mode]]*Num_IM # 0 for running mode and 9999.9 for park mode
ServoDyn_Value[10] = [TimGenOf[Mode]]*Num_IM  # 9999.9 for running mode and 0 for park mode
ServoDyn_Value[11] = [TPCOn[Mode]]*Num_IM
ServoDyn_Value[12] = [HSSBrMode[Mode]]*Num_IM
ServoDyn_Value[13] = [THSSBrDp[Mode]]*Num_IM
# InflowWind
File_InflowWind = '{}_InflowWind.dat'.format(Name)
Path_InflowWind = Path_OpenFAST
# Parallel
os.chdir(Path_OpenFAST)
for IM_i in range(Num_IM):
    FilePath = Destination + '/{}mps'.format(str(TurbSim_Value[0][IM_i]))
    if not os.path.isdir(FilePath):
        os.mkdir(FilePath)
    Parallel(n_jobs=NOP)(delayed(IM_Analysis)(num+1, File_OpenFAST, Name, Path_OpenFAST, FilePath, OpenFAST_exe, TurbSim_exe,
                                              File_TurbSim, Path_TurbSim, TurbSim_Str, [TV[IM_i] for TV in TurbSim_Value],
                                              File_HydroDyn, Path_HydroDyn, HydroDyn_Str, [HV[IM_i] for HV in HydroDyn_Value],
                                              File_ElastoDyn, Path_ElastoDyn, ElastoDyn_Str, [EV[IM_i] for EV in ElastoDyn_Value],
                                              File_ServoDyn, Path_ServoDyn, ServoDyn_Str, [SV[IM_i] for SV in ServoDyn_Value],
                                              File_InflowWind, Path_InflowWind)
                         for num in range(Num_Records))
