import matplotlib.pyplot as plt
import HelperFunctions
from scipy.signal import hilbert
import numpy as np

'''
    This test is intented to test if nyquist frequency type effects are at play by
    artificalally increasing the "sampling rate" through interpolation 
'''


energy, slog, phase = HelperFunctions.get_processed_data()

point_count = np.asarray([5e3,1e4, 1e6, 1e7], int)

for n in point_count:
    elin, slin = HelperFunctions.interpolate_list(energy, slog, n)
    phaseH = -np.imag(hilbert(slin))
    plt.plot(elin, phaseH, label= "Point # "+ HelperFunctions.human_format(n))

phaseH = -np.imag(hilbert(slog))
plt.plot(energy,phaseH, label = "Uninterpolated")
plt.plot(energy,phase, label = "TDSE")
HelperFunctions.graph_setup_EP()

plt.savefig("../Plots/interpolationTest")
plt.show()
