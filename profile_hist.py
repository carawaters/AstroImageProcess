import matplotlib.pyplot as plt
import numpy as np
from profile import int_radius, sersic_index, sersic
from astropy.io import fits

hdulist = fits.open('A1_mosaic.fits')
data = hdulist[0].data
hdulist.close()

data = data[5:, :]

noise_mean = 3419
noise_std = 12
val_min = noise_mean + 4 * noise_std

sers = np.loadtxt("sersic_indices.csv", delimiter=',')
sers = sers[sers <= 10]

coord = (646, 73)

intensity = int_radius(data, coord, val_min)
n, k = sersic_index(intensity[1:])
I_0 = intensity[0]

radius = np.array(range(1, len(intensity)))
plt.figure(2)
plt.plot(np.log(radius), np.log(intensity[1:]), 'x')
pts = np.linspace(min(radius), max(radius), 100)
plt.plot(np.log(pts), sersic(pts, I_0, k,  n))
plt.xlabel("ln(R)")
plt.ylabel("ln(I)")

plt.figure(1)
plt.hist(sers[~np.isnan(sers)], bins=20)
plt.ylabel("Count")
plt.xlabel("Sersic index (n)")
plt.grid()
plt.show()