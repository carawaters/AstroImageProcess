import numpy as np
from astropy.io import fits

hdulist = fits.open('A1_mosaic.fits')

print(hdulist[0].header)
print(hdulist[0].data)

hdulist.close()