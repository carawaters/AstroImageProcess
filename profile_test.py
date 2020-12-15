from profile import int_radius, sersic_index
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits

hdulist = fits.open('A1_mosaic.fits')
data = hdulist[0].data
hdulist.close()

data = data[5:, :]

noise_mean = 3419
noise_std = 12
val_min = noise_mean + 4 * noise_std
edge_noise = 100

points = np.genfromtxt('points.csv', delimiter=',')

sersic_indices = []

num = 1

for point in points:
    print(num)
    cent = (int(point[0]), int(point[1]))
    print(cent)
    if cent[0] >= len(data[1])-edge_noise or cent[0] <= edge_noise or cent[1] >= len(data[0])-edge_noise or cent[1] <= edge_noise:
        sersic_indices.append(np.NaN)
    else:
        intensity = int_radius(data, cent, val_min)
        if len(intensity) <= 3:
            sersic_indices.append(np.NaN)
        else:
            print(intensity)
            n, k = sersic_index(intensity)
            sersic_indices.append(n)
    num += 1

np.savetxt('sersic_indices.csv', np.array(sersic_indices), delimiter=',')