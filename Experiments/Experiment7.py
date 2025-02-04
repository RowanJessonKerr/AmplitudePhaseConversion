import matplotlib.pyplot as plt
import HelperFunctions
from scipy.signal import hilbert
import numpy as np
from hilbert_toolkit import hilbert_fft_henrici


#Reduced Hilbert Transform
energy, Sint, phase = HelperFunctions.get_data()
Ry = 13.6058
energy = energy*2*Ry
Elin, Sint  = HelperFunctions.interpolate_list(energy, Sint, int(1e6))

C = max(Sint)

Sint += C
print(max(Sint))
Slog = np.log(Sint)

Sh = hilbert(Slog)
hilbert_phase = np.imag(Sh)

Rhilbert_tan_phase = Sint*np.sin(hilbert_phase)/(Sint*np.cos(hilbert_phase)-C)
Rhilbert_phase = np.atan(Rhilbert_tan_phase)

Rhilbert_phase = np.unwrap(Rhilbert_phase,discont=0.1,period=np.pi/2) + np.pi/2

plt.plot(energy,phase)
plt.plot(Elin,Rhilbert_phase)
HelperFunctions.graph_setup_EP()
plt.show()


#Modified Hilbert Transform

energy, Slog, phase = HelperFunctions.get_processed_data()
Elin, Sint  = HelperFunctions.interpolate_list(energy, Slog, int(1e6))

Mh = hilbert(Sint/Elin)  
Mhilbert_phase = np.imag(Mh)*Elin+np.pi/2
plt.plot(Elin, Mhilbert_phase)
#HelperFunctions.graph_setup_EP()

plt.show()


#Modified Hilbert Transform
energy, Slog, phase = HelperFunctions.get_processed_data()
hilb = hilbert_fft_henrici(Slog) 
func = - energy / np.pi * (hilb/energy - hilb[0]/energy)
plt.plot(energy,func)
#HelperFunctions.graph_setup_EP()
plt.plot()
plt.show()