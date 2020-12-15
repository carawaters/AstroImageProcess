"""
Calculates the Sersic index for every point identified
"""
from profile import int_radius, sersic_index
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits

hdulist = fits.open('A1_mosaic.fits')
data = hdulist[0].data
hdulist.close()

data = data[5:, :]

noise_mean = 3419
noise_std = 12
val_min = noise_mean + 4 * noise_std
edge_noise = 100

points = np.genfromtxt('points.csv', delimiter=',')

sersic_indices = []

#loop through each point and fit to find sersic index
for point in points:
    cent = (int(point[0]), int(point[1]))
    #check not too close to edge so excluding noise
    if cent[0] >= len(data[1])-edge_noise or cent[0] <= edge_noise or cent[1] >= len(data[0])-edge_noise or cent[1] <= edge_noise:
        sersic_indices.append(np.NaN)
    else:
        intensity = int_radius(data, cent, val_min)
        #radius must be >= 3 to give enough points to plot
        if len(intensity) <= 3:
            sersic_indices.append(np.NaN)
        else:
            n, k = sersic_index(intensity)
            sersic_indices.append(n)

np.savetxt('sersic_indices.csv', np.array(sersic_indices), delimiter=',')