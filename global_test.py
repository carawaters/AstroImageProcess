"""
A series of tests for the global detection of galaxies.
"""
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from numpy import random

#load fits file
hdulist = fits.open('A1_mosaic.fits')

header = hdulist[0].header
data = hdulist[0].data

hdulist.close()

#header.totextfile(open('header.txt', 'wb'))

#image of all zeros
zeros = np.full_like(data, 0)

#image with all below noise threshold
low_noise = np.full_like(data, 3000)

#image with 'bleeding' objects

#adding in Gaussian 'blobs' FWHM ~1 arcsecond

no_blobs = 100

x_mid = np.random.randint(low=0, high=np.amax(data.shape[0]), size=no_blobs) #generates random x and y centres for blobs
y_mid = np.random.randint(low=0, high=np.amax(data.shape[1]), size=no_blobs)

blobs = np.full_like(data, 0)
cov = np.array([[1.65, 0], [0, 1.65]]) #sigma based off FWHM and resolution

#for i in range(no_blobs+1):
    #x, y = np.random.default_rng().multivariate_normal(np.array([x_mid[i], y_mid[i]]), cov)
    #blobs = 5000*x

#different shapes of galaxies