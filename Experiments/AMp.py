import matplotlib.pyplot as plt
import HelperFunctions
from scipy.signal import hilbert
import numpy as np

energy, amp, phase = HelperFunctions.get_data()

plt.plot(energy, amp)
HelperFunctions.graph_setup_EA(xlim=False)
plt.savefig("../Plots/AmpOG")
plt.show()