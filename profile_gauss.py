"""
Creates a Gaussian profile and fits a Sersic profile to the intensity
Author: Cara Waters
Date: 15/12/20
"""
import numpy as np
import matplotlib.pyplot as plt
from numpy import random
from profile import int_radius, sersic_index, sersic

def makeGaussian(amp, sigma, center):
    """
    Makes a symmetric 2D gaussian.
    Inputs: amp = amplitude multiplier (float), sigma = standard deviation (list length 2), center = central point location (list length 2)
    Output: array of 2D gaussian values
    """
    x = np.arange(0, 100, 1)
    y = x[:,np.newaxis]
    x0 = center[0]
    y0 = center[1]
    sig_x = sigma[0]
    sig_y = sigma[1]

    return amp * np.exp(-(((x - x0)**2/(2*sig_x**2))+((y - y0)**2/(2*sig_y**2))))

#Intializing sigma and mu
amp = 30000
sigma = [5, 5]
center = [50, 50]
  
#Calculating Gaussian array 
gauss = makeGaussian(amp, sigma, center)
data = gauss
data = data.astype(int)

intensity = int_radius(data, (50,50), 5000)
n, k = sersic_index(intensity)
I_0 = intensity[0]

radius = np.array(range(0, len(intensity)))

fig, ax = plt.subplots(2, 1, figsize=(5, 10))
ax[0].imshow(data, label=("2D Gaussian, sigma= " + str(sigma)))
ax[0].set_title("2D Gaussian, sigma= " + str(sigma))

ax[1].plot(radius, sersic(radius, I_0, k, n), label="Sersic profile, n = " + str(round(n, 2)) + ", k = " + str(round(k, 2)))
ax[1].plot(radius, np.log(intensity), 'rx')
ax[1].set_xlabel("Radius (R)")
ax[1].set_ylabel("ln(I)")
ax[1].legend()
ax[1].grid()
plt.show()