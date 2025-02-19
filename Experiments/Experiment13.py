import matplotlib.pyplot as plt
import HelperFunctions
from scipy.signal import hilbert
import numpy as np
from hilbert_toolkit import hilbert_fft_henrici
from scipy.interpolate import make_interp_spline

'''
    This expirment is to test the MHT method and attempt to get it to work
    It uses the gaussian extension from expirment10 and RHT from 7
'''

energy, Sint, phase = HelperFunctions.get_data()
Ry = 13.6058
energy = energy *2*Ry

Sint *= 1e8
def extension(x):
    c = 4 * np.log(2)/ np.log(2.71)
    b = 2.10132
    g = 48.5523
    t = 50.35
    return b*np.exp(-c *(x-t)**2/g**2)

extensionRange = np.linspace(energy[0], energy[-1] + 50, int(1000000))
filt = np.logical_and(extensionRange < energy[-1], extensionRange>energy[0])

interp_xsection = make_interp_spline(energy, Sint, 2)

Sintp = interp_xsection(extensionRange) 
Sinte = extension(extensionRange)
fullSint = np.where(filt, Sintp, Sinte)

#Reduced Hilbert Transform
Slog = np.log(fullSint)


a = np.linspace(1000,10000,1000000)
plt.scatter(extensionRange, Slog/(a), s=0.1)
plt.show()

hilbert_phase = -a**2 / np.pi*hilbert_fft_henrici((Slog/(a**2)))

hilbert_phase = np.unwrap(hilbert_phase,discont=0.1,period=np.pi/2)

plt.plot(extensionRange,hilbert_phase)
plt.plot(energy,phase)
#HelperFunctions.graph_setup_EP()
plt.show()


