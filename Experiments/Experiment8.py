import matplotlib.pyplot as plt
from scipy.signal import hilbert
import numpy as np

'''
    This is a simple test of the behaviour  of the hilbert transform. 
    The goal was to get a feel for edge effects 
'''

x = np.linspace(-1, np.pi * 2, 10000)

cos = np.cos(x)
sin = np.sin(x)
sinH = np.imag(hilbert(cos))

plt.plot(x, cos, label = "cos")
plt.plot(x, sin, label = "sin")
plt.plot(x, sinH, label = "$\\mathcal{H}[cos]$")
plt.legend()
plt.show()

fft = np.fft.fft(cos)
fffreq = np.fft.fftfreq(len(cos), x[1] - x[0])

plt.scatter(fffreq, fft, s=0.1)
plt.show()