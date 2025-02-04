import matplotlib.pyplot as plt
from scipy.signal import hilbert
import numpy as np

x = np.linspace(-1, np.pi * 2, 10000)

cos = np.cos(x)
sin = np.sin(x)
sinH = np.imag(hilbert(cos))

plt.plot(x, cos, label = "cos")
plt.plot(x, sin, label = "sin")
plt.plot(x, sinH, label = "$\\mathcal{H}[cos]$")
plt.legend()
plt.show()