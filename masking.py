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

data = data[2250:4250, 500:2500]
print(data)

#detect objects by pixel value, min = mean + 4 std devs = 3467
val_min = 3467
val_max = 5400

#function to give a circular mask dependent on radius
def create_circular_mask(width, height, centre, radius):
    x, y = np.ogrid[:width, :height]

    dist_from_centre = np.sqrt((x - centre[0])**2 + (y - centre[1])**2)
    mask = dist_from_centre <= radius

    return mask

width = data.shape[0]
height = data.shape[1]

thresh = 20000

#set up overall mask
bright_points = data[data >= thresh]
indices = np.nonzero(data >= thresh)
current_mask = np.array(np.logical_or(data >= val_max, data <= val_min), dtype=bool)
print(len(bright_points))

plt.figure(1)
plt.imshow(current_mask, cmap='binary')
plt.colorbar()
ymin, ymax = plt.ylim()
plt.ylim(ymax, ymin)

#find points around brightest point to exclude
for i in range(len(bright_points)):
    coord = (indices[0][i], indices[1][i])
    brightness = data[coord[0], coord[1]]
    j = 0
    while brightness >= val_min:
        if coord[1]+j == data.shape[0]:
            break
        else:
            brightness = data[coord[0], coord[1]+j]
            j += 1
    circ = create_circular_mask(width, height, coord, j)
    current_mask = np.logical_or(current_mask, circ)
    print(i)

plt.figure(2)
plt.imshow(data, cmap = 'gray', norm=LogNorm())
plt.colorbar()
ymin, ymax = plt.ylim()
plt.ylim(ymax, ymin)

plt.figure(3)
plt.imshow(current_mask, cmap='binary')
plt.colorbar()
ymin, ymax = plt.ylim()
plt.ylim(ymax, ymin)
plt.show()