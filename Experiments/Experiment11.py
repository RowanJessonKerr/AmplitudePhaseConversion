import matplotlib.pyplot as plt
import HelperFunctions
from scipy.signal import hilbert
import numpy as np
from hilbert_toolkit import hilbert_fft_henrici
from scipy.interpolate import make_interp_spline
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

'''
    This is a basic test to remove numberical instablity 
    by multiplying the cross section by a big number. Uses the extension of 10 and RHT of 7
'''

energy, Sint, phase = HelperFunctions.get_data()
Ry = 13.6058
energy = energy *2*Ry

Sint *= 1e8 #To reduce numerical instablity 
def extension(x):
    c = 4 * np.log(2)/ np.log(2.71)
    b = 0.210131 * 10
    g = 48.5523
    t = 50.35
    return b*np.exp(-c *(x-t)**2/g**2)

extensionRange = np.linspace(energy[0], energy[-1] + 50, int(100000))
filt = np.logical_and(extensionRange <= energy[-1], extensionRange>=energy[0])

interp_xsection = make_interp_spline(energy, Sint, 2)

Sintp = interp_xsection(extensionRange) 
Sinte = extension(extensionRange)
fullSint = np.where(filt, Sintp, Sinte)


fig, ax = plt.subplots(dpi = 300)

ax.plot(extensionRange[filt], Sintp[filt], label = "TDSE")
ax.plot(extensionRange[np.logical_not(filt)], Sinte[np.logical_not(filt)], label = "Gaussian Extension")

HelperFunctions.graph_setup_EA(xlim=False)

axins = zoomed_inset_axes(ax, 50, loc=1, bbox_to_anchor=(1.1, 0.95), bbox_transform=ax.transAxes)


x1, x2, y1, y2 = 81, 82, 0.62, 0.7
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)

axins.plot(extensionRange[filt], Sintp[filt], label = "TDSE")
axins.plot(extensionRange[np.logical_not(filt)], Sinte[np.logical_not(filt)], label = "Gaussian Extension")

mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")

ax.legend(loc="upper left")

plt.savefig("../Plots/AmplitudeGaussianExtension")
plt.show()

#Reduced Hilbert Transform

C =  5
SintA = fullSint + C
Slog = np.log(SintA)

Sh = hilbert(Slog)
hilbert_phase = -np.imag(Sh)

Rhilbert_tan_phase = SintA*np.sin(hilbert_phase)/(SintA*np.cos(hilbert_phase)-C)
Rhilbert_phase = np.atan(Rhilbert_tan_phase)

Rhilbert_phase = np.unwrap(Rhilbert_phase,discont=0.1,period=np.pi/2)

plt.plot(energy,phase, label = "TDSE")
plt.plot(extensionRange,Rhilbert_phase , label = "RLHT")

interp_Psection = make_interp_spline(extensionRange, Rhilbert_phase, 2)
interpt = interp_Psection(energy)

HelperFunctions.graph_setup_EP()
plt.savefig("../Plots/RHTGExtension")
plt.show()
