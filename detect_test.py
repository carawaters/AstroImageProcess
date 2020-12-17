"""
Carries out a test on a data set for masking unwanted pixels and catalogueing objects
Author: Cara Waters
Date: 4/12/20
"""
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from masking import bright_mask, catalogue

#thresholds for object masking and detection
noise_mean = 3419
noise_std = 12
val_min = noise_mean + 6 * noise_std
val_max = 5400
radius = 15 #Radius of area seen around point and of mask produced after catalogueing
thresh = 30000

hdulist = fits.open('A1_mosaic.fits')

header = hdulist[0].header
data = hdulist[0].data
hdulist.close()

#Cropping out bottom bleed
data = data[5:, :]

width = data.shape[0]
height = data.shape[1]

#Mask bright objects and make a catalog
current_mask = bright_mask(data, thresh, val_min, noise_mean, noise_std, width, height)
catalog = catalogue(data, current_mask, radius, width, height, 'points_6std.csv')

#Plot of identified objects
plt.figure(1)
plt.imshow(data, cmap = 'gray', norm=LogNorm())
plt.plot(*zip(*catalog), 'rx', markersize=5)
plt.colorbar()
ymin, ymax = plt.ylim()
plt.ylim(ymax, ymin)

#Plot of mask
plt.figure(2)
plt.imshow(current_mask, cmap='binary')
plt.colorbar()
ymin, ymax = plt.ylim()
plt.ylim(ymax, ymin)
plt.show()