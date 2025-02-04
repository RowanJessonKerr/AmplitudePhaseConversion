import matplotlib.pyplot as plt
import HelperFunctions
from scipy.signal import hilbert
import numpy as np

'''
    This experiment is to test if the issues with the Hilbert transform calculation are only
    present in amplitude to phase calculations
'''

energy, slog, phase = HelperFunctions.get_processed_data()

slogH = np.imag(hilbert(phase))

plt.plot(energy, slogH, label  = "LHT")
plt.plot(energy, slog, label ="TDSE")
HelperFunctions.graph_setup_EA()
plt.savefig("../Plots/PhaseToAmp")
plt.show()

plt.plot(energy, slogH, label  = "LHT")
plt.plot(energy, slog + 20, label ="TDSE")
HelperFunctions.graph_setup_EA()
plt.savefig("../Plots/PhaseToAmpShifted")
plt.show()

