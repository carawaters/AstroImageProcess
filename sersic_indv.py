"""
Fits a Sersic profile to an individual object
Author: Cara Waters
Date: 16/12/20
"""
import matplotlib.pyplot as plt
import numpy as np
from profile import int_radius, sersic_index, sersic, find_cent
from astropy.io import fits

#position and noise parameters
coord = (2387, 847)
noise_mean = 3419
noise_std = 12
val_min = noise_mean + 4 * noise_std

hdulist = fits.open('A1_mosaic.fits')
data = hdulist[0].data
hdulist.close()

data = data[5:, :]

#find fit parameters for profile
cent = find_cent(data, coord)
intensity = int_radius(data, coord, val_min)
n, k = sersic_index(intensity)
radius = np.array(range(0, len(intensity)))

plt.plot(radius, np.log(intensity), 'rx')
plt.plot(radius, sersic(radius, intensity[0], k, n))
plt.show()