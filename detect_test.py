import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from masking import bright_mask, catalogue

#thresholds for object masking and detection
noise_mean = 3419
noise_std = 12
val_min = noise_mean + 4 * noise_std
val_max = 5400
radius = 15 #Radius of area seen around point and of mask produced after catalogueing
thresh = 35000

hdulist = fits.open('A1_mosaic.fits')

header = hdulist[0].header
data = hdulist[0].data
hdulist.close()

data = data[5:, :]

width = data.shape[0]
height = data.shape[1]

current_mask = bright_mask(data, thresh, val_min, noise_mean, noise_std, width, height)
catalog = catalogue(data, current_mask, radius, width, height, 'catalog_35000.csv')

plt.figure(1)
plt.imshow(data, cmap = 'gray', norm=LogNorm())
plt.plot(*zip(*catalog), 'rx', markersize=5)
plt.colorbar()
ymin, ymax = plt.ylim()
plt.ylim(ymax, ymin)

plt.figure(2)
plt.imshow(current_mask, cmap='binary')
plt.colorbar()
ymin, ymax = plt.ylim()
plt.ylim(ymax, ymin)
plt.show()