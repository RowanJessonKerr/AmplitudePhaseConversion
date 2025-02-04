import matplotlib.pyplot as plt
import HelperFunctions
from scipy.signal import hilbert
import numpy as np
'''
    This Expirment is to see the inital issue that we are trying to solve with this project
'''

Energy, Slog, Phase = HelperFunctions.get_processed_data()

phaseH = -np.imag(hilbert(Slog))

plt.plot(Energy, phaseH, label = "He Standard LHT", color = 'r')
plt.plot(Energy, Phase, label = "He TDSE")
HelperFunctions.graph_setup_EP()


plt.savefig("../Plots/InitalPhaseToAmp")
plt.show()