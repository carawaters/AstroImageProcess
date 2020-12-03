"""
Masks image to indicate prescence of objects.
"""

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

hdulist = fits.open('A1_mosaic.fits')

header = hdulist[0].header
data = hdulist[0].data

hdulist.close()

#generate array of same shape
mask = np.full_like(data, 0)

#detect objects by pixel value, max = 30000, min = mean + 4 std devs = 3467
val_min = 3467
val_max = 10000

for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        pixel = data[i,j]
        if pixel >= val_min and pixel < val_max:
            mask[i,j] = 1
        else:
            mask[i,j] = 0

plt.figure(1)
plt.imshow(data, cmap = 'gray', norm=LogNorm())
plt.colorbar()
ymin, ymax = plt.ylim()
plt.ylim(ymax, ymin)

plt.figure(2)
plt.imshow(mask, cmap='gray')
plt.colorbar()
ymin, ymax = plt.ylim()
plt.ylim(ymax, ymin)
plt.show()