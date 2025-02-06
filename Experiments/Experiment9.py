import matplotlib.pyplot as plt
import HelperFunctions
from scipy.signal import hilbert
import numpy as np
from hilbert_toolkit import hilbert_fft_henrici

'''
    This Experiment is testing if padding the input signal is helpful.
    This is built from the RLHT method from Experiment7
'''

#Reduced Hilbert Transform
energy, Sint, phase = HelperFunctions.get_data()
Ry = 13.6058
energy = energy*2*Ry
Elin, Sint  = HelperFunctions.interpolate_list(energy, Sint, int(1e6))

padRight = 500000
padLeft = 5000
Sint = np.pad(Sint, (0,padRight), 'reflect', reflect_type='odd')
Sint = np.pad(Sint, (padLeft,0), 'reflect', reflect_type='odd')

Elin = HelperFunctions.linear_extend(Elin, left_pad=padLeft ,right_pad=padRight)

C = 1
SintA = Sint + C
Slog = np.log(SintA)

plt.plot(Elin,Sint)
plt.savefig("../Plots/PaddingExtensionOfCrossSection")
plt.show()

Sh = hilbert(Slog)
hilbert_phase = np.imag(Sh)

Rhilbert_tan_phase = SintA*np.sin(hilbert_phase)/(SintA*np.cos(hilbert_phase)-C)
Rhilbert_phase = np.atan(Rhilbert_tan_phase)

Rhilbert_phase = np.unwrap(Rhilbert_phase,discont=0.1,period=np.pi/2) + np.pi/2

plt.plot(energy,phase, label = "TDSE")
plt.plot(Elin,-Rhilbert_phase , label = "RLHT")
HelperFunctions.graph_setup_EP()
plt.savefig("../Plots/RLHTransformPaded")
plt.show()