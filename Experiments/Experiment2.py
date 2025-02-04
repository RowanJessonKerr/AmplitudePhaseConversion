import matplotlib.pyplot as plt
import HelperFunctions
from scipy.signal import hilbert
import numpy as np

'''
    This experiment is to check if the hilbert function correctly shows the inverse properity that 
    the hilbert funtion mathematically has. That is  H[H[f]] = -f
'''

energy, Slog, Phase =  HelperFunctions.get_processed_data()

phaseH = -np.imag(hilbert(Slog))
ampHH = np.imag(hilbert(phaseH))

plt.plot(energy, ampHH, label = "$-\\mathcal{H}[\\mathcal{H}[\\phi]]$" ,color = 'r')
plt.plot(energy,Slog, label = "Log(|f|)")

HelperFunctions.graph_setup_EA()

plt.savefig("../Plots/InverseTest")
plt.show()

plt.plot(energy, ampHH, label = "$-\\mathcal{H}[\\mathcal{H}[\\phi]]$" ,color = 'r')
plt.plot(energy,Slog- np.mean(Slog), label = "Log(|f|)")

HelperFunctions.graph_setup_EA()
plt.savefig("../Plots/InverseTestShifted")
plt.show()