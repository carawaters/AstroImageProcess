import matplotlib.pyplot as plt
import numpy as np
from profile import int_radius, sersic_index, sersic
from astropy.io import fits
from matplotlib.ticker import MaxNLocator

hdulist = fits.open('A1_mosaic.fits')
data = hdulist[0].data
hdulist.close()

data = data[5:, :]

#set params
noise_mean = 3419
noise_std = 12
val_min = noise_mean + 4 * noise_std

sers = np.loadtxt("sersic_indices_35000.csv", delimiter=',')
sers = sers[sers <= 20]

#Histogram of sersic indices for all objects possible to calc for
ax = plt.figure(1).gca()
plt.hist(sers[~np.isnan(sers)], bins=20, edgecolor='black', linewidth=1.2, color='lightblue')
plt.ylabel("Count")
plt.xlabel("Sersic index (n)")
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_axisbelow(True)
plt.grid()
plt.savefig('sersic_index_hist', dpi=300)
plt.show()