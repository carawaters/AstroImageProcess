import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from photometry import circ_apt_flux

def int_radius(data, cent, val_min):
    """
    Returns an array of the intensity at different radii out from the centre of an object
    """
    val = data[cent]
    rad = 0
    while val >= val_min:
        if rad >= 7:
            break
        val = data[cent[0], cent[1]+rad]
        rad += 1
    intensity = []
    for r in range(1, rad+1):
        flux, _ = circ_apt_flux(data, cent, r*2)
        I_r = flux/(np.pi*(r**2))
        intensity.append(I_r)
    return np.array(intensity)

def sersic(radius, I_0, k, n):
    """
    The Sersic profile to fit
    """
    return np.log(I_0) - k * radius**(1/n)

def sersic_index(intensity):
    """
    Fits the Sersic profile to return the Sersic index for an object
    """
    radius = np.array(range(0, len(intensity)))
    I_0 = intensity[0]
    popt, pcov = curve_fit(lambda radius, k, n: sersic(radius, I_0, k, n), radius, np.log(intensity), p0=[0.5, 5])
    n = popt[1]
    k = popt[0]
    return n, k