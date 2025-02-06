import matplotlib.pyplot as plt
import HelperFunctions
from scipy.signal import hilbert
import numpy as np
from hilbert_toolkit import hilbert_fft_henrici

'''
    This Experiment is to test if removing the zeros of the 
    cross section which are at zero and infinte energy improves the acuracy. 
'''

#Reduced Hilbert Transform
energy, Sint, phase = HelperFunctions.get_data()
Ry = 13.6058
energy = energy*2*Ry
Elin, Sint  = HelperFunctions.interpolate_list(energy, Sint, int(1e6))

C = 1
SintA = Sint + C

Slog = np.log(Sint)
SlogAdjusted = np.log(SintA)

Sh = hilbert(SlogAdjusted)
hilbert_phase = np.imag(Sh)

Rhilbert_tan_phase = SintA*np.sin(hilbert_phase)/(SintA*np.cos(hilbert_phase)-C)
Rhilbert_phase = np.atan(Rhilbert_tan_phase)

Rhilbert_phase = np.unwrap(Rhilbert_phase,discont=0.1,period=np.pi/2)

DirectHilbert = -hilbert_fft_henrici(Slog)

plt.plot(energy,phase, label = "TDSE")
plt.plot(Elin,Rhilbert_phase , label = "RLHT")
plt.plot(Elin, DirectHilbert, label = "LHT")
HelperFunctions.graph_setup_EP()
plt.savefig("../Plots/RLHTransform")
plt.show()