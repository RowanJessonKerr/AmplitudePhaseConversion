import matplotlib.pyplot as plt
import HelperFunctions
import numpy as np
from hilbert_toolkit import hilbert_fft_henrici
from scipy.interpolate import make_interp_spline

'''
    This extends the shape of the amplitude using a gaussian fitted to 
    the large gaussian like structure with peak around E=50eV. RHT is used from 7
'''

energy, Sint, phase = HelperFunctions.get_data()
Ry = 13.6058
energy = energy *2*Ry

def extension(x):
    c = 4 * np.log(2)/ np.log(2.71)
    b = 0.210132e-7
    g = 48.5523
    t = 50.35
    return b*np.exp(-c *(x-t)**2/g**2)

extensionRange = np.linspace(energy[0], energy[-1] + 40, int(1e7))
filt = extensionRange < energy[-1]

interp_xsection = make_interp_spline(energy, Sint, 2)

Sintp = interp_xsection(extensionRange[filt]) 
Sinte = extension(extensionRange[np.logical_not(filt)])
fullSint = np.append(Sintp, Sinte)

plt.plot(extensionRange, fullSint)
plt.show()

Slog = np.log(fullSint)

phaseH = -hilbert_fft_henrici(Slog)
plt.plot(extensionRange,phaseH)
plt.plot(energy, phase)
plt.show()