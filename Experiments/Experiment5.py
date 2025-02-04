import matplotlib.pyplot as plt
import HelperFunctions
from scipy.signal import hilbert
import numpy as np

from hilbert_toolkit import hilbert_fft_henrici
from hilbert_toolkit import hilbert_fft_marple
from hilbert_toolkit import hilbert_haar
from hilbert_toolkit import hilbert_pad_simple
from hilbert_toolkit import hilbert_pad_wrap

def my_hilbert(f):
    fft = np.fft.fft(f)
    fftfreq = np.fft.fftfreq(len(f))

    step = [-1 if w<0 else 1 for w in fftfreq]
    multi = [0 if w==0 else 1 for w in fftfreq]
    fullstep = step * multi

    adjustedfft = 1j * fullstep * fft
    return np.fft.ifft(adjustedfft)

energy, slog, phase = HelperFunctions.get_processed_data()

henrici = -hilbert_fft_henrici(slog)
marple = -hilbert_fft_marple(slog)
haar = -hilbert_haar(slog)
pad_simple = -hilbert_pad_simple(slog,hilbert_fft_henrici)

plt.plot(energy, henrici, label = "henrici")
plt.plot(energy, marple, label = "marple")
plt.plot(energy, haar, label = "haar")
plt.plot(energy, pad_simple, label = "pad_simple")
plt.plot(energy, phase, label = "Actual ")

HelperFunctions.graph_setup_EP()
plt.savefig("/Plots/HilbertMethods")
plt.show()




