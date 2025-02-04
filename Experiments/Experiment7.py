import matplotlib.pyplot as plt
import HelperFunctions
from scipy.signal import hilbert
import numpy as np

energy, Sint, phase = HelperFunctions.get_data()
Elin, Sint  = HelperFunctions.interpolate_list(energy, Sint, int(1e6))

Sint += 1 
Slog = np.log(Sint)

Sh = hilbert(Slog/2)       #RHT
Mh = hilbert(Slog/2/Elin)  #MHT 

hilbert_phase = np.imag(Sh)
Mhilbert_phase = np.imag(Mh)*Elin+np.pi/2

plt.plot(np.imag(Mh))
plt.show()

C = 1

Rhilbert_tan_phase = Sint*np.sin(hilbert_phase)\
                          /(Sint*np.cos(hilbert_phase)-C)
Rhilbert_phase = -np.atan(Rhilbert_tan_phase)+np.pi/2

Rhilbert_phase = np.unwrap(Rhilbert_phase,discont=0.1,period=np.pi/2)-np.pi

#plt.plot(energy,phase)
#plt.plot(Elin,Rhilbert_phase)
plt.plot(Elin, Mhilbert_phase)

plt.show()