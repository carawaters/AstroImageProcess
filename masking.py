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

data = data[2500:3500, 1000:2000]
print(data)

#thresholds for object masking and detection
noise_mean = 3419
noise_std = 12
val_min = noise_mean + 4 * noise_std
val_max = 5400

#function to give a circular mask dependent on radius
def create_circular_mask(width, height, centre, radius):
    x, y = np.ogrid[:width, :height]

    dist_from_centre = np.sqrt((x - centre[0])**2 + (y - centre[1])**2) #find min distance to check if within radius
    mask = dist_from_centre <= radius

    return mask

width = data.shape[0]
height = data.shape[1]

thresh = 20000

#set up overall mask
bright_points = data[data >= thresh]
indices = np.nonzero(data >= thresh)
current_mask = np.array(data <= val_min, dtype=bool)

bright_min = noise_mean + 2.5 * noise_std

#find points around brightest point to exclude
for i in range(len(bright_points)):
    coord = (indices[0][i], indices[1][i])
    brightness = data[coord[0], coord[1]]
    j = 0
    while brightness >= bright_min:
        if coord[1]+j == data.shape[0]: #check for edge case
            break
        else:
            brightness = data[coord[0], coord[1]+j]
            j += 1
    circ = create_circular_mask(width, height, coord, j) #mask inside of bright object
    current_mask = np.logical_or(current_mask, circ)
    print(i)

#Points to use for catalog
cat_pts = data[np.logical_not(current_mask)] #mask True when excluding so need to remember what we need for current use
cat_indices = np.nonzero(np.logical_not(current_mask))
cat_mask = current_mask
radius = 20 #Radius of area seen around point and of mask produced after catalogueing

catalog = []

for a in range(len(cat_pts)):
    coord = (cat_indices[0][a], cat_indices[1][a])
    if cat_mask[coord] == True:
        pass
    else:
        init_brightness = data[coord[0], coord[1]]
        obj_mask = create_circular_mask(width, height, coord, radius)
        obj_pts = data*obj_mask #use mask as 1/0 to give only points within range of stars
        cent = np.unravel_index(np.argmax(obj_pts), obj_pts.shape)
        catalog.append((cent[1], cent[0])) #indices reversed for plotting due to indexing being reversed
        excl_mask = create_circular_mask(width, height, cent, radius)
        cat_mask = np.logical_or(cat_mask, excl_mask) #exclude points of object from being checked again

print(catalog)
np.savetxt('catalog.csv', catalog, delimiter=',')

fig1, ax1 = plt.subplots(1, 1)
plt.imshow(data, cmap = 'gray', norm=LogNorm())
plt.plot(*zip(*catalog), 'rx', markersize=5)
plt.colorbar()
ymin, ymax = plt.ylim()
plt.ylim(ymax, ymin)
plt.show()