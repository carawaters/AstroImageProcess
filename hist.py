"""
Fits a Gaussian profile to the background of the image
Author: Cara Waters
Date: 27/11/20
"""
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

hdulist = fits.open('A1_mosaic.fits')

header = hdulist[0].header
data = hdulist[0].data

hdulist.close()

#remove high values
data_small = data[data < 10000].flatten()

#gaussian to fit
def func(x, mu, std, a):
    return a * np.exp(-np.power((x - mu), 2)/(2*std**2))

plt.figure(1)
#histogram with 5000 bins from testing
n, bins, _ = plt.hist(data_small, bins=5000, color='orange')

#generate bin centres
points = []
for i in range(1, len(bins)):
    points.append(bins[i-1] + (bins[i]-bins[i-1])/2)

popt, pcov = curve_fit(func, points, n, p0=[3410, 50, 700000])

plt.plot(points, func(points, *popt), 'k', linewidth = 2, label = "Mean: " + str(int(round(popt[0], 0))) + " Std: " + str(int(round(popt[1], 0))))
plt.xlim()
plt.xlabel('Pixel Value')
plt.ylabel('Count')
plt.legend()
plt.grid()
plt.savefig('images/noise_hist', dpi=300, bbox_inches='tight')

plt.show()