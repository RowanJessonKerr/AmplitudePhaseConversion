import matplotlib.pyplot as plt
import HelperFunctions
from scipy.signal import hilbert
import numpy as np

'''
    Since mathematically the Hilbert Transform is deeply connected to the Fourier I wanted to 
    look at the Fourier Transform of the hilbert and measured phases.
'''

energy, slog, phase = HelperFunctions.get_processed_data()

phaseH = - np.imag(hilbert(slog))

fftH = np.fft.fft(phaseH)
fftP = np.fft.fft(phase)
freqs = np.fft.fftfreq(len(phase))


np.savetxt("fourierTransform.csv", np.column_stack((freqs, np.real(fftH), np.real(fftP))), delimiter=',')

plt.scatter(freqs, np.real(fftH), s= 0.1, label = "$\\mathcal{F[H[}f]]$")
plt.scatter(freqs, np.real(fftP), s= 0.1, label = "$\\mathcal{F[[\\phi]]}$")
plt.legend()
plt.title("Fourier's of Phase: Real Component")
plt.xlabel("Frequency")
#plt.xlim([-0.08,0.08])
plt.ylim([-200,100])
plt.ylabel("Amplitude Real Component")
plt.savefig("../Plots/FourierRealPhase")
plt.show()

plt.scatter(freqs, np.imag(fftH), s= 0.1, label = "$\\mathcal{F[H[}f]]$")
plt.scatter(freqs, np.imag(fftP), s= 0.1, label = "$\\mathcal{F[[\\phi]]}$")
plt.legend()
plt.title("Fourier's of Phase: Imaginary Component")
plt.xlabel("Frequency")
plt.xlim([-0.06,0.06])
plt.ylim([-150,150])
plt.ylabel("Amplitude Imag Component")
plt.savefig("../Plots/FourierImagPhase")

plt.show()

e, s = HelperFunctions.interpolate_list(energy, slog, 50000)

fftSlog = np.fft.fft(s)
freqs = np.fft.fftfreq(len(s), d=(e[1] - e[0]))
powerSpec = np.abs(fftSlog)

plt.scatter(freqs, powerSpec, s=0.1)

plt.title("Power Spectrum of $log|f|$")
plt.xlabel("Frequency")
plt.ylabel("Power")
plt.show()