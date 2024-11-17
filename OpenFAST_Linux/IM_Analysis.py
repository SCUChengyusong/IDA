import numpy as np
import subprocess
import os
import shutil
from FileModification import FM
def IM_Analysis(num, File_OpenFAST, Name, Path_OpenFAST, Destination, File_TurbSim, Path_TurbSim, TurbSim_Str, TurbSim_Val,
                File_HydroDyn, Path_HydroDyn, HydroDyn_Str, HydroDyn_Val, File_ElastoDyn, Path_ElastoDyn, ElastoDyn_Str, ElastoDyn_Val,
                File_ServoDyn, Path_ServoDyn, ServoDyn_Str, ServoDyn_Val, File_InflowWind, Path_InflowWind):
    WindSpeed = str(TurbSim_Val[0])
    RandSeeds = np.random.randint(-2147483648, 2147483647, 4)

    TurbSim_Str.extend(['RandSeed1', 'RandSeed2'])
    TurbSim_Val.extend([str(RandSeeds[0]), str(RandSeeds[1])])
    FM(File_TurbSim, Path_TurbSim, TurbSim_Val, TurbSim_Str, WindSpeed, num)

    HydroDyn_Str.extend(['WaveSeed(1)', 'WaveSeed(2)'])
    HydroDyn_Val.extend([str(RandSeeds[2]), str(RandSeeds[3])])
    FM(File_HydroDyn, Path_HydroDyn, HydroDyn_Val, HydroDyn_Str, WindSpeed, num)

    FM(File_ElastoDyn, Path_ElastoDyn, ElastoDyn_Val, ElastoDyn_Str, WindSpeed, num)

    FM(File_ServoDyn, Path_ServoDyn, ServoDyn_Val, ServoDyn_Str, WindSpeed, num)

    Name_TurbSim = File_TurbSim.split('.')[0]
    InflowWind_Value = ['InflowData/{}mps_{}_{}.bts'.format(WindSpeed, num, Name_TurbSim)]
    InflowWind_Str = ['FileName_BTS']
    FM(File_InflowWind, Path_InflowWind, InflowWind_Value, InflowWind_Str, WindSpeed, num)

    OpenFAST_Value = ['{}mps_{}_{}'.format(WindSpeed, num, File_HydroDyn), '{}mps_{}_{}'.format(WindSpeed, num, File_ElastoDyn),
                      '{}mps_{}_{}'.format(WindSpeed, num, File_ServoDyn), '{}mps_{}_{}'.format(WindSpeed, num, File_InflowWind)]
    OpenFAST_Str = ['HydroFile', 'EDFile', 'ServoFile', 'InflowFile']
    FM(File_OpenFAST, Path_OpenFAST, OpenFAST_Value, OpenFAST_Str, WindSpeed, num)

    with open(Path_OpenFAST + '/{}mps_{}_{}_out.txt'.format(WindSpeed, num, Name), 'a+', encoding='UTF-8') as out:
        subprocess.run(['turbsim', Path_TurbSim + '/{}mps_{}_{}'.format(WindSpeed, num, File_TurbSim)], stdout=subprocess.PIPE)
        subprocess.run(['openfast', Path_OpenFAST + '/{}mps_{}_{}'.format(WindSpeed, num, File_OpenFAST)], stdout=out)
    out.close()

    shutil.copyfile(Path_OpenFAST + '/{}mps_{}_{}.out'.format(WindSpeed, num, Name),
                    Destination + '/{}mps'.format(WindSpeed) + '/{}_data.txt'.format(str(num)))
    shutil.copyfile(Path_OpenFAST + '/{}mps_{}_{}.sum'.format(WindSpeed, num, Name),
                    Destination + '/{}mps'.format(WindSpeed) + '/{}_sum.txt'.format(str(num)))
    shutil.copyfile(Path_OpenFAST + '/{}mps_{}_{}_out.txt'.format(WindSpeed, num, Name),
                    Destination + '/{}mps'.format(WindSpeed) + '/{}_out.txt'.format(str(num)))

    os.remove(Path_TurbSim + '/{}mps_{}_{}'.format(WindSpeed, num, File_TurbSim))
    os.remove(Path_TurbSim + '/{}mps_{}_{}.sum'.format(WindSpeed, num, Name_TurbSim))
    os.remove(Path_TurbSim + '/{}mps_{}_{}.bts'.format(WindSpeed, num, Name_TurbSim))
    os.remove(Path_HydroDyn + '/{}mps_{}_{}'.format(WindSpeed, num, File_HydroDyn))
    os.remove(Path_ElastoDyn + '/{}mps_{}_{}'.format(WindSpeed, num, File_ElastoDyn))
    os.remove(Path_ServoDyn + '/{}mps_{}_{}'.format(WindSpeed, num, File_ServoDyn))
    os.remove(Path_InflowWind + '/{}mps_{}_{}'.format(WindSpeed, num, File_InflowWind))
    os.remove(Path_OpenFAST + '/{}mps_{}_{}'.format(WindSpeed, num, File_OpenFAST))
    os.remove(Path_OpenFAST + '/{}mps_{}_{}.out'.format(WindSpeed, num, Name))
    os.remove(Path_OpenFAST + '/{}mps_{}_{}.sum'.format(WindSpeed, num, Name))
    os.remove(Path_OpenFAST + '/{}mps_{}_{}_out.txt'.format(WindSpeed, num, Name))
