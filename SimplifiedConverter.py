import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert
from scipy import fft as sp_fft

#load cross-section
file_lines = []
with open(sys.argv[1], 'r') as i:
    for l in i:

        l = " ".join(l.split())+'\n'
        file_lines.append(l)

data = np.genfromtxt(file_lines, delimiter = ' ', comments = '##' and '#')

#get energy cross section and phas from file
Energy = data[:,0]
CrossSection = data[:,1] ## Probably not techniqually cross section, acutally amplitude.
Phase = data[:,3]


SLog = np.log(np.abs(CrossSection))

hilb = hilbert(SLog)
phase = -np.imag(hilb)

#plt.scatter(sp_fft.fftfreq(len(phase)),sp_fft.fft(phase), label = "LHT", s=0.1)
plt.scatter(sp_fft.fftfreq(len(Phase)),sp_fft.fft(Phase), label = "TDSE", s=0.1)
plt.legend()
plt.savefig("Plots/FourierTransforms")
plt.show()