import sys
import numpy as np
from scipy.interpolate import make_interp_spline
from matplotlib import pyplot as plt

def get_data():
    '''
    Returns lists Energy, Amplitude, Phase
    '''
    #load cross-section
    file_lines = []
    with open(sys.argv[1], 'r') as i:
        for l in i:

            l = " ".join(l.split())+'\n'
            file_lines.append(l)

    data = np.genfromtxt(file_lines, delimiter = ' ', comments = '##' and '#')

    return data[:,0], data[:,1], data[:,3]

def get_processed_data():
    '''
    Returns energy, logarithmic amplitude, phase
    '''
    Ry = 13.6058
    energy, amplitude, phase = get_data()
    energy = energy *2*Ry
    Slog = np.log(amplitude)
    return  energy, Slog, phase

def interpolate_list(x, f , numpoints, interp_order = 2):
    '''
    returns the interpolated x and f list, where f is a function of x
    '''
    interp_xsection = make_interp_spline(x, f, interp_order)
    xlin = np.linspace(x[0], x[-1], numpoints) 
    fint = interp_xsection(xlin) 
    return xlin, fint


def graph_setup_EP(xlim = True):
    '''
    Sets Graph details for energy-phase plots
    '''
    plt.title("Energy - Phase")
    plt.xlabel('Photoelectron energy ω (eV)')
    plt.ylabel('Hilbert phase, rad')
    plt.legend()

    if xlim:
        plt.xlim([2,6])

def graph_setup_EA(xlim = True):
    '''
    Sets Graph details for energy-amplitude plots
    '''
    plt.title("Energy - Ionisation Amplitude")
    plt.xlabel('Photoelectron energy ω (eV)')
    plt.ylabel('Amplitude (arb. units)')
    plt.legend()
    if xlim:
        plt.xlim([2,6])

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

