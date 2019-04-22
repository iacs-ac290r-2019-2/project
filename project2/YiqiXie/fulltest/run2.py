#!/usr/bin/env python

'''
Simulation: 
Drug released in blood vessel with stenosis

Input:
 - blood: bgkflag.1 (.hdr, .dat, .ios)
 - drug:  bgkflag.2 (.hdr, .dat, .ios)

Time:
 - NPERIOD = 1e6
 - NSTEP = 4 * NPERIOD

Geometry:
Vessel: 
 - R = ?
 - L = 20 * R
Stenosis: 
 - G = 1/2 * R
 - S = 1/10 * L
 - A = 1/2 * L
Bolus:  
 - W = 1/20 * L
 - B = 1/4 * L

Matter:
Drug:
 - D = ?
 - C_in(t) = 0.01
 - C_out(t) = 0.01
 - C_bolus(0) = 1
Blood:
 - nu = 0.1
 - ubar = 0.01
 - u_in(t) = 1/2 * ubar * (1 + cos(2*pi*t / NPERIOD))
 - p_out(t) = 0
 
Characteristics:
 - Re = ubar * 2R / nu
 - Pe = ubar * R  / D
 - Pr = nu / D
Tune Re, Pe with proper choice of {R, D}

'''

from MagicUniverse import *
import sys
import math

# preprocess_parallel_mesh(4); sys.exit(1)

RE = 2.         # reynold number
PE = 10.        # peclet  number
PR = 2.*PE/RE   # prandtl number

RHO  = 1.       # blood density
UBAR = 0.01     # blood half-max speed
NU   = 0.1      # blood viscosity
D    = NU/PR    # drug diffusitivy

R = D*PE/UBAR   # vessel radius
L = R*20.       # vessel length
W = L/20.       # width of bolus
B = L/4.        # x-pos of bolus

C0 = 0.01       # initial concentration at the boundary
C1 = 1.         # initial concentration in the bolus

NPERIOD  = int(1e6)
NSTEP    = int(4e3)
NDIAG    = int(1e2)
NVTKFREQ = int(1e2)

MagicBegins()

# define universe

u = Universe()
s = Scale()
m = Mesh()
f = Fluid()     # blood
c = Fluid()     # drug
t = Tracker()

# u.addItems([s,m,f,t])
u.addItems([s,m,f,c,t])

u.setTitle('DrugRelease')
u.setNumberOfSteps(NSTEP)
u.setStateRestart(False)
u.setStateDumpFrequency(-1)

u.create()

# set params

# s.set(name='MonoScale', mesh=m, actors=[f,t])
s.set(name='MonoScale', mesh=m, actors=[f,c,t])
m.setRegularMesh(True)
m.setPeriodicity('000')
m.setDomainDecomposition(1)
# m.setDomainDecomposition(7)
# m.setPartitionAlongXYZ(2,2,256) # for 1024 cores

t.setDiagnosticFrequency(NDIAG)
# t.setDataShow(density=True, velocity=True)
# t.setMapDirections('zx')
t.setVtkDump(True, frequency=NVTKFREQ)

f.setName('Blood')
f.setViscosity(NU)
f.setDensityUniform(RHO)
f.setInletOutletMethod('equilibrium')
f.setInletOutletFile('bgkflag.1.ios')
f.setStabilizeLB(True)
f.setFreeze(False)

c.setName('Drug')
c.setDiffusivity(D)
c.setInletOutletMethod('equilibrium')
c.setInletOutletFile('bgkflag.2.ios')
c.setStabilizeLB(True)
c.setFreeze(True)

u.decorate()

nx, ny, nz = m.getBox()
nx = int(nx)
ny = int(ny)
nz = int(nz)
profile2 = c.getArray(nx*ny*nz) 
for k in xrange(1, nz+1):
    for j in xrange(1, ny+1):
        for i in xrange(1, nx+1):
            ifl = m.getLocator(i,j,k)
            if k-1 > (nz-1)/L*(B-W/2) and k-1 < (nz-1)/L*(B+W/2):
                profile2[ifl] = C1
            else:
                profile2[ifl] = C0
c.setDensityProfile(profile2)

for itime in u.cycle():
    f.setIOValue('inlet',  1, 0.5*UBAR*(1+math.cos(2*math.pi*itime/NPERIOD)))
    f.setIOValue('outlet', 2, 0.)
    c.setIOValue('inlet',  1, C0)
    c.setIOValue('outlet', 2, C0)
    if itime == 1000:
        c.setFreeze(False)
    u.animate()

MagicEnds()
