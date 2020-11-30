import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from astropy.io import fits

hdulist = fits.open('A1_mosaic.fits')

header = hdulist[0].header
data = hdulist[0].data

hdulist.close()

plt.imshow(data, cmap = 'gray', norm=LogNorm())
plt.colorbar()
ymin, ymax = plt.ylim()
plt.ylim(ymax, ymin)
plt.show()