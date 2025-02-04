#Restricted and modified Hilbert transform as in
#Burge et al (1974,1976)

import sys
import math
from math import *
import numpy as np
from scipy import interpolate
from scipy.ndimage import gaussian_filter as gf
from matplotlib import pyplot as plt
from scipy import linalg, fft as sp_fft
from scipy.signal import hilbert, chirp

from unwrap import *
            
#♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪  Main program  ♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪
# Takes RPAE input for Xe augmented by the Coulomb phase♪ 
# first command line argument is the input file name    ♪ 
# -pd takes phase difference of #6 and #10 else just #6 ♪
# Example: burge.py Xe4df -pd                           ♪ 
#♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪
  
#load data
file_lines = []
with open(sys.argv[1], 'r') as i:  #Open file for reading
    for l in i:
        l = " ".join(l.split())+'\n'
        file_lines.append(l)

data = np.genfromtxt(file_lines, delimiter = ' ', comments = '#')

#Constants
Ry = 13.6058; atto = 24.2
IP = 4.964 *Ry


#get energy cross section and phase from file
E = data[:,0] #Energy
S = data[:,1] #Cross-section HF-L


if ('-pd' in sys.argv):
    datafile_phase = data[:,5] - data[:,9]
else:
    datafile_phase = data[:,5]

#maximum of cross section/energy
SEmax  = np.max(S/E)

#get cross section phase
xsection_phase = np.arcsin(np.minimum(1.0,np.sqrt(S/(E*SEmax))))
xsection_phase = unwrap(xsection_phase)

#INTERPOLATE CROSS-SECTION TO LINEAR GRID

xsection_int =interpolate.interp1d(E, S, kind='quadratic')
N = 100000    #number of interpolation points
Elin = np.linspace(E[0], E[-1], N) #linear energy grid
dE = (E[-1]-E[0])/N #energy step
Sint = xsection_int(Elin)
print('Size', len(S), len(Sint))
print('Boundaries', E[0], E[-1])

#♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦
#LOGARITHMIC CROSS-SECTION 
#♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦

#Add a constant    
C  = 30
C = 1
Sint = Sint + C

Slog = np.empty(N, dtype=object)
for i in range(N):
    Slog[i] = math.log(Sint[i])

#♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠
#CROSS-SECTION PLOT
#♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠

plt.figure(figsize=(4,3))
##plt.plot(E, S, label = 'Xe 4d raw', color = 'r')
##plt.plot(Elin, Sint,label='interpolated',linestyle='dotted',color ='g')
#Log cross-section
plt.plot(Elin, Slog, label = 'Log', color = 'b',linestyle = 'dashed')
plt.xlim([60, 140])#; plt.ylim([-0.5, 0.5])
plt.legend()
plt.xlabel('Photon energy ω (eV)')
plt.ylabel('Cross-section')
plt.show()
##exit() 
#Hilbert transform
Sh = hilbert(Slog/2)       #RHT
Mh = hilbert(Slog/2/Elin)  #MHT 
hilbert_phase = np.imag(Sh)
Mhilbert_phase = np.imag(Mh)*Elin+pi/2

Rhilbert_tan_phase = np.empty(N, dtype=object)
Rhilbert_phase = np.empty(N, dtype=object)

for i in range(N):
    Rhilbert_tan_phase[i] = Sint[i]*math.sin(hilbert_phase[i])\
                          /(Sint[i]*math.cos(hilbert_phase[i])-C)
    Rhilbert_phase[i] = math.atan(Rhilbert_tan_phase[i])+pi/2

Rhilbert_phase = np.unwrap(Rhilbert_phase,discont=0.1,period=pi/2)-pi

#♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥
#HILBERT PHASE PLOT
#♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥

plt.figure(figsize=(4,3))
#plt.xlim([69, 140]);plt.ylim([0, 3.5])
plt.plot(E, datafile_phase, label = 'Xe 4d->Ef phase')
plt.plot(E, xsection_phase, label = 'cross section phase')
plt.plot(Elin, Rhilbert_phase, label = 'RHilbert phase C=30',\
         color = 'b',linestyle = 'dashed')
##plt.plot(Elin, Mhilbert_phase, label = 'MHilbert phase C=1',\
##         color = 'g',linestyle = 'dashed')
plt.xlabel('Energy (eV)')
plt.ylabel('phase (rad)')
plt.legend()
plt.show()

#¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤
#WRITE PHASE TO A FILE
#¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤

f = open("RHphase.txt", "w")
##f = open("MHphase.txt", "w")
f.write("#Phase via restricted Hilbert transform C=30\n")
##f.write("#Phase via modified Hilbert transform C=1\n")
f.write("#Energy (eV) Phase (rad) \n")
for i in range(N):
    f.write(f"{Elin[i]:.8}");f.write(" ");\
                f.write(f"{Rhilbert_phase[i]:.6}\n")
f.close()

