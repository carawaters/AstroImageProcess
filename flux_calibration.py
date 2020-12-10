import numpy as np
from astropy.io import fits

hdulist = fits.open('A1_mosaic.fits')


header = hdulist[0].header
data = hdulist[0].data

hdulist.close()

from photometry import flux
data_small = data[1450:1500,1200:1230]
counts = flux(data_small)
m = header["MAGZPT"] -2.5*np.log10(counts)
print(m)
