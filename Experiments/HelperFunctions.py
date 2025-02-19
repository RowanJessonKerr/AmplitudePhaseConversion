import sys
import numpy as np
from scipy.interpolate import make_interp_spline
from scipy.interpolate import interp1d
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

#https://stackoverflow.com/questions/40642061/how-to-set-axis-ticks-in-multiples-of-pi-python-matplotlib
def multiple_formatter(denominator=2, number=np.pi, latex='\pi'):
    def gcd(a, b):
        while b:
            a, b = b, a%b
        return a
    def _multiple_formatter(x, pos):
        den = denominator
        num = int(np.rint(den*x/number))
        com = gcd(num,den)
        (num,den) = (int(num/com),int(den/com))
        if den==1:
            if num==0:
                return r'$0$'
            if num==1:
                return r'$%s$'%latex
            elif num==-1:
                return r'$-%s$'%latex
            else:
                return r'$%s%s$'%(num,latex)
        else:
            if num==1:
                return r'$\frac{%s}{%s}$'%(latex,den)
            elif num==-1:
                return r'$\frac{-%s}{%s}$'%(latex,den)
            else:
                return r'$\frac{%s%s}{%s}$'%(num,latex,den)
    return _multiple_formatter
#https://stackoverflow.com/questions/40642061/how-to-set-axis-ticks-in-multiples-of-pi-python-matplotlib
class Multiple:
    def __init__(self, denominator=2, number=np.pi, latex='\pi'):
        self.denominator = denominator
        self.number = number
        self.latex = latex

    def locator(self):
        return plt.MultipleLocator(self.number / self.denominator)

    def formatter(self):
        return plt.FuncFormatter(multiple_formatter(self.denominator, self.number, self.latex))


def graph_setup_EP(xlim = True):
    '''
    Sets Graph details for energy-phase plots
    '''
    plt.title("Energy - Phase")
    plt.xlabel('Photoelectron energy ω (eV)')
    plt.ylabel('Hilbert phase, rad')
    plt.legend()

    ax = plt.gca()

    y_min, y_max = ax.get_ylim()

    # Enforce max limit of [-2π, 2π] only if exceeded
    if y_min < -2*np.pi or y_max > 2*np.pi:
        ax.set_ylim(np.clip([y_min, y_max], -2*np.pi, 2*np.pi))

    ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(np.pi / 12))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(multiple_formatter()))

    if xlim:
        plt.xlim([1,6])

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


#https://stackoverflow.com/questions/579310/formatting-long-numbers-as-strings
def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

#ChatGPT
def linear_extend(arr, left_pad, right_pad):
    x = np.arange(len(arr))  # Original indices
    y = arr  # Original values
    
    # Create an extrapolation function
    f = interp1d(x, y, kind='linear', fill_value='extrapolate')
    
    # Generate new indices for left and right padding
    left_indices = np.arange(-left_pad, 0)
    print(len(left_indices))
    right_indices = np.arange(len(arr), len(arr) + right_pad)
    
    # Compute the extrapolated values
    left_extension = f(left_indices)
    right_extension = f(right_indices)
    
    return np.concatenate([left_extension, arr, right_extension])

    


