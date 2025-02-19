import matplotlib.pyplot as plt
import HelperFunctions
from scipy.signal import hilbert
import numpy as np
from hilbert_toolkit import hilbert_fft_henrici
from scipy.interpolate import make_interp_spline

'''
    This is an attempt to avoid numerical instablity by dividing by the underlying 
    gaussian. This uses RHT from 7. Note if C=0 the orginal LHT phase is recovered 
'''

energy, Sint, phase = HelperFunctions.get_data()
Ry = 13.6058
energy = energy *2*Ry

def extension(x):
    c = 4 * np.log(2)/ np.log(2.71)
    b = 0.210132 * 1e-7
    g = 48.5523
    t = 50.35
    return b*np.exp(-c *(x-t)**2/g**2)


Eint, Sint = HelperFunctions.interpolate_list(energy, Sint, 10000)
Sint /= extension(Eint)

padLeft = 10000
padRight = 10000

fullSint = np.pad(Sint,(padLeft,padRight), 'constant', constant_values=(1,1))
extensionRange = HelperFunctions.linear_extend(Eint,padLeft,padRight)

plt.plot(extensionRange, fullSint)
plt.show()

#Reduced Hilbert Transform

C = 1000
SintA = fullSint + C
Slog = np.log(SintA)

Sh = hilbert(Slog)
hilbert_phase = -np.imag(Sh)

Rhilbert_tan_phase = SintA*np.sin(hilbert_phase)/(SintA*np.cos(hilbert_phase)-C)
Rhilbert_phase = np.atan(Rhilbert_tan_phase)

Rhilbert_phase = np.unwrap(Rhilbert_phase,discont=0.1,period=np.pi/2)

plt.plot(energy,phase, label = "TDSE")
plt.plot(extensionRange,Rhilbert_phase , label = "RLHT")
HelperFunctions.graph_setup_EP()

plt.savefig("../Plots/GaussianNormalised")
plt.show()