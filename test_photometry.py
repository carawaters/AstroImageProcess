"""
Maike Lenz, 08/12/20
Tests the photometry functions on a test data set with one bright pixel at x=30, y=20
"""
import numpy as np
#defining the test data sets
test1=3419*np.ones((50,50)) #should not be able to find anything
test2=np.copy(test1)
test2[20][30] = 50000 #test2 brightest pixel is at (20,30)
test2[20][38] = 30000
apt_size=12
ann_size=5
from photometry import find_max, circ_apt_flux, ann_ref, flux

centre=find_max(test2)
print(centre) #returns [20,30] which is correct
print(circ_apt_flux(test2, centre, apt_size)) #returns total flux 432928, and N=113 as expected
print(ann_ref(test2,centre,apt_size,ann_size)) #returns 3419 as expected, with Na=263, so the 30000 pixel has been excluded
print(flux(test2, centre, apt_size, ann_size)) #returns 46581 as expected



mean,data_small_ref=ann_ref(data_small, find_max(data_small),12,5)
plt.imshow(data_small_ref, cmap = 'gray', norm=LogNorm())
plt.colorbar()
ymin, ymax = plt.ylim()
plt.ylim(ymax, ymin)
plt.show() #prints test section