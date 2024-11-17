# -*- coding: utf-8 -*
import openseespy.opensees as op
import numpy as np
import math
from Loading_Series import Loading_Series

def Monopile_Build(Nodes, Elements, Sections, Aero_Twr, Load_Path, Result_Path, MYS, WF, WS):
    Record_Path = (Load_Path + str(WS) + 'mps/' + str(WF) + '_data.txt')
    ksi = 0.01
    op.wipe()
    op.model('basic', '-ndm', 3, '-ndf', 6)
    [op.node(i + 1, float(Nodes.X[i]), float(Nodes.Y[i]), float(Nodes.Z[i])) for i in range(len(Nodes))]
    op.fix(1, 1, 1, 1, 1, 1, 1)
    op.uniaxialMaterial('Steel02', 1, MYS, 2.1E11, 0.01, 18.0, 0.925, 0.15)
    for i in range(len(Sections)):
        op.section('Fiber', i + 1, '-GJ', Sections.GJ[i])
        op.patch('circ', 1, 18, 3, 0.0, 0.0, Sections.R_in[i], Sections.R_out[i], 0.0, 360.0)
    op.geomTransf('Linear', 1, 1, 1, 1)
    for i in range(len(Elements)):
        op.beamIntegration('Legendre', i + 1, int(Elements.Section[i]), 5)
        op.element('forceBeamColumn', i + 1, int(Elements.Node1[i]), int(Elements.Node2[i]), 1, i + 1)
    op.rigidLink('beam', 56, 57)
    [op.mass(i + 1, Nodes.Mass[i], Nodes.Mass[i], Nodes.Mass[i], 0.0, 0.0, 0.0) for i in range(len(Nodes))]
    Eigen = op.eigen('genBandArpack', 4)
    Omega = [math.pow(Eigen[i], 0.5) for i in range(len(Eigen))]
    # Fre = [Omega[i] / 2 / math.pi for i in range(len(Omega))]
    # print(' f1 = ' + str(Fre[0]), '\n', 'f2 = ' + str(Fre[2]))
    a0 = 2 * ksi * (Omega[0] * Omega[2]) / (Omega[0] + Omega[2])
    a1 = 2 * ksi / (Omega[0] + Omega[2])
    op.rayleigh(a0, a1, 0.0, 0.0)
    dt = 0.05
    Nodes_Rot = [57]
    Nodes_Twr = Aero_Twr.Node
    Nodes_Fod = [11]
    Col_Rot = np.array([41, 42]) - 1  # Rotor
    Col_Twr = np.arange(23, 41, 1) - 1  # Tower
    Col_Fod = np.array([44, 45]) - 1  # Foundation
    DOF_Load_x = [1, 0, 0, 0, 0, 0]
    DOF_Load_y = [0, 1, 0, 0, 0, 0]
    Time, Dic_Rot, Dic_Twr, Dic_Fod = Loading_Series(Record_Path, Col_Rot, Col_Twr, Col_Fod, Aero_Twr)
    [op.timeSeries('Path', 101 + i, '-dt', dt, '-values', *Dic_Rot[i], '-time', *Time, 'startTime', 0.0) for i in
     range(len(Col_Rot))]  # Rotor
    [op.timeSeries('Path', 201 + i, '-dt', dt, '-values', *Dic_Twr[i], '-time', *Time, 'startTime', 0.0) for i in
     range(len(Col_Twr))]  # Tower
    [op.timeSeries('Path', 301 + i, '-dt', dt, '-values', *Dic_Fod[i], '-time', *Time, 'startTime', 0.0) for i in
     range(len(Col_Fod))]  # Foundation
    for i in range(int(len(Col_Rot)/2)):  # Rotor
        op.pattern('Plain', 101 + i, 101 + i)
        op.load(int(Nodes_Rot[i]), *DOF_Load_x)
    for i in range(int(len(Col_Rot)/2)):  # Rotor
        op.pattern('Plain', 102 + i, 102 + i)
        op.load(int(Nodes_Rot[i]), *DOF_Load_y)
    for i in range(int(len(Col_Twr)/2)):  # Tower
        op.pattern('Plain', 201 + i, 201 + i)
        op.load(int(Nodes_Twr[i]), *DOF_Load_x)
    for i in range(int(len(Col_Twr)/2)):  # Tower
        op.pattern('Plain', 210 + i, 210 + i)
        op.load(int(Nodes_Twr[i]), *DOF_Load_y)
    for i in range(int(len(Col_Fod)/2)):  # Foundation
        op.pattern('Plain', 301 + i, 301 + i)
        op.load(int(Nodes_Fod[i]), *DOF_Load_x)
    for i in range(int(len(Col_Fod)/2)):  # Foundation
        op.pattern('Plain', 302 + i, 302 + i)
        op.load(int(Nodes_Fod[i]), *DOF_Load_y)

    op.recorder('Node', '-file', (Result_Path + str(WF) + '_TwrTopDisp.txt'), '-node', 56, '-dof', *[1, 2], 'disp')
    
    op.wipeAnalysis()
    op.constraints('Transformation')
    op.numberer('Plain')
    op.system('Umfpack')
    op.test('NormDispIncr', 1.0e-5, 1000, 0)
    op.algorithm('BFGS')
    op.integrator('Newmark', 0.5, 0.25)
    op.analysis('Transient')
    numIncr = len(Time)
    op.analyze(numIncr, dt)
    op.remove('recorders')
