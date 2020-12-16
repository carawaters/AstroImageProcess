"""
Contains functions for finding the intensity at a range of radii and the Sersic index of an object
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from photometry import circ_apt_flux, circ_mask, find_max

def find_cent(data, cent):
    """
    Finds the true center of the object
    """
    mask = circ_mask(data, cent, 12)
    data_set = data * np.logical_not(mask)
    new_cent = find_max(data_set)
    print(new_cent)
    return new_cent

def int_radius(data, cent, val_min):
    """
    Returns an array of the intensity at different radii out from the centre of an object
    """
    val = data[tuple(cent)]
    print(val)
    rad = 0
    #finding max radius for calculating intensity
    while val >= val_min:
        #need to make sure we don't get infinity
        if rad >= 20:
            break
        val = data[cent[0], cent[1]+rad]
        rad += 1
    intensity = []
    #find intensity within circle of each radius
    for r in range(1, rad+1):
        flux, N = circ_apt_flux(data, cent, r*2)
        print(N)
        I_r = flux/N
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
    #lambda function to make I_0 a fixed value as we already know it
    popt, pcov = curve_fit(lambda radius, k, n: sersic(radius, I_0, k, n), radius, np.log(intensity), p0=[0.5, 5])
    n = popt[1]
    k = popt[0]
    return n, k