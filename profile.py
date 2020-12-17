"""
Contains functions for finding the intensity at a range of radii and the Sersic index of an object
Author: Cara Waters
Date: 14/12/20
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from photometry import circ_apt_flux, circ_mask, find_max

def find_cent(data, cent):
    """
    Finds the true center of the object by the brighest pixel in case of not being identified properly
    Inputs: data = the image data (2D numpy array), cent = the centre point in the catalog (list or tuple length 2)
    Output: new_cent = new centre point (list length 2)
    """
    mask = circ_mask(data, cent, 12)
    data_set = data * np.logical_not(mask)
    new_cent = find_max(data_set)
    return new_cent

def int_radius(data, cent, val_min):
    """
    Returns an array of the intensity at different radii out from the centre of an object
    Inputs: data = the image data (2D numpy array), cent = the centre point of the object (list or tuple length 2),
            val_min = minimum threshold for radius of object (int)
    Output: intensity = list of intensities for increasing radius from centre (1D numpy array)
    """
    val = data[tuple(cent)]
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
        I_r = flux/N
        intensity.append(I_r)
    return np.array(intensity)

def sersic(radius, I_0, k, n):
    """
    The Sersic profile to fit
    Inputs: radius = the radius at which to give intensity included (int), I_0 = intensity at centre (int),
            k = multiplying factor for fit (float), n = sersic index (float)
    Ouput: log(I) = intensity at radius provided (int)
    """
    return np.log(I_0) - k * radius**(1/n)

def sersic_index(intensity):
    """
    Fits the Sersic profile to return the Sersic index for an object
    Input: intensity = the intensity included within each radius from the centre (numpy array)
    Outputs: n = sersic index (float), k = multiplying factor for fit (float)
    """
    radius = np.array(range(0, len(intensity)))
    I_0 = intensity[0]
    #lambda function to make I_0 a fixed value as we already know it
    popt, pcov = curve_fit(lambda radius, k, n: sersic(radius, I_0, k, n), radius, np.log(intensity), p0=[0.5, 5])
    n = popt[1]
    k = popt[0]
    return n, k