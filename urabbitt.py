#python urabbitt.py craq -> craq.lht
#                   575c -> 575c.lht
#                   abc.h2 
import sys
import math  
from math import *
import numpy as np
from scipy import interpolate
from scipy.ndimage import gaussian_filter as gf
from matplotlib import pyplot as plt
from scipy.signal import hilbert, chirp
from scipy import linalg, fft as sp_fft

#CONSTANTS
Ry = 13.6058
asec = 24.2
ip = 24.6


#load cross-section
file_lines = []
with open(sys.argv[1], 'r') as i:
    for l in i:

        l = " ".join(l.split())+'\n'
        file_lines.append(l)

data = np.genfromtxt(file_lines, delimiter = ' ', comments = '##' and '#')

#get energy cross section and phas from file
E = data[:,0]
S = data[:,1]
F = data[:,3]

if ('abc.h2' in sys.argv):
    K = data[:,1]
    A = data[:,2]; A = A*K
    B = data[:,4]; B = B*K
    F = data[:,6]
    S = B
    
E = E*2*Ry
Emin = 10;Emax = 20
name = 'H\u2082'

if ('craq' in sys.argv):
    Emin = 2;Emax = 6
    name = 'He'

#interpolate cross-section
interp_xsection  =interpolate.interp1d(E, S, kind='quadratic')


N = 10000    #number of interpolation points
Elin = np.linspace(E[0], E[-1], N) #linear energy scale
dE = (E[-1]-E[0])/N #energy scale
print('Energy', E[0],E[-1])
print('target', name)
Sint = interp_xsection(Elin) #linear interp

#Add a constant    
##C  = 0.1e-6
##Sint = Sint + C

Slog = np.empty(N, dtype=object)
for i in range(N):
    Slog[i] = abs(math.log(Sint[i]))
                  
#==================
#CROSS-SECTION PLOT
#==================

plt.figure(figsize=(4.7,3.7))
plt.rcParams.update({'font.size': 9})

if ('abc.h2' in sys.argv):
    plt.plot(E, A*1e6, label =  name + " A",color = 'b')
    plt.plot(E, B*1e6, label =  name + " B",color = 'r')
else:
    plt.plot(E, S*1e6, label =  name + " TDSE",color = 'b')


plt.plot(Elin, Sint*1e6, label = 'Interpolated',color = 'g',linestyle = 'dashed')

plt.xlim([0, 6])#;plt.ylim([0, 2])
plt.xlim([Emin, Emax])
plt.legend()
plt.xlabel('Photoelectron energy ω (eV)')
##plt.ylabel('Angular anisotropy β')
plt.ylabel('Amplitude (arb. units)')
plt.show()

##print('STOP', XXXXXX)

Sh = hilbert(Slog)
hilbert_phase = np.imag(Sh)

##Rhilbert_tan_phase = np.empty(N, dtype=object)
##Rhilbert_phase = np.empty(N, dtype=object)
##
##for i in range(N):
##    Rhilbert_tan_phase[i] = Sint[i]*math.sin(hilbert_phase[i])\
##                          /(Sint[i]*math.cos(hilbert_phase[i])-C)
##    Rhilbert_phase[i] = math.atan(Rhilbert_tan_phase[i])+pi/2
##
##Rhilbert_phase = -np.unwrap(Rhilbert_phase,discont=0.1,period=pi/2)+3*pi/2

#==========
#PHASE PLOT
#==========

plt.figure(figsize=(4.7,3.7))
plt.rcParams.update({'font.size': 9})
plt.plot(E, F, label =  name +" TDSE",color = 'b')
plt.plot(Elin, hilbert_phase, label = name + " LHT",\
         color = 'r',linestyle = 'solid')
##plt.plot(Elin, Rhilbert_phase, label = 'RHilbert phase C=30',\
##         color = 'g',linestyle = 'dashed')

plt.xlim([Emin, Emax])
plt.legend()
plt.xlabel('Photoelectron energy ω (eV)')
plt.ylabel('Hilbert phase, rad')
plt.show()


#==============♪================#
# WRITE PHASE and DELAY TO FILE #
#==============♪================#

f = open(sys.argv[1]+".lht", "w")
##f = open("MHphase.txt", "w")
f.write(f"#")
f.write(f"{sys.argv[1]}\n")
f.write("#Interpolation points=");f.write(f"{N:1}\n")
f.write("#Energy (eV) Phase (rad)\n ")
for i in range(N):
    f.write(f"{Elin[i]:.8}");f.write(" ");\
    f.write(f"{hilbert_phase[i]:.6}\n")
f.close()



