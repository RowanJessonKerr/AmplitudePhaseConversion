import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

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

Ry = 13.6058
Energy = Energy*2*Ry

Emin = 2;Emax = 6
name = 'He'
plt.figure(figsize=(4.7,3.7))
plt.rcParams.update({'font.size': 9})


SLog = np.log(np.abs(CrossSection))

fftSLog = np.fft.fft(SLog)
freqs = np.fft.fftfreq(len(SLog))
stepfunction = np.array([-1 if f < 0 else 1 for f in (freqs)])


slogHFFT = -1j * stepfunction * np.fft.fft(Phase)
slogH = np.fft.ifft(slogHFFT)



plt.scatter(freqs, np.imag(fftSLog), s= 0.1)
plt.scatter(freqs, np.imag(slogHFFT), s= 0.1)

plt.show()

full = slogH + 1j * Phase
plt.scatter(freqs,np.fft.fft(full), s=0.1 )

plt.legend()
plt.title("Testing Mathematical Accuracy of Computation")
plt.xlabel("x")
plt.ylabel("y")
plt.show()