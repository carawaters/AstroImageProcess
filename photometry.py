import numpy as np
from astropy.io import fits
hdulist = fits.open('A1_mosaic.fits')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

header = hdulist[0].header
data = hdulist[0].data

hdulist.close()
data_small = data[1430:1500,1180:1230]

"""
plt.imshow(data_small, cmap = 'gray', norm=LogNorm())
plt.colorbar()
ymin, ymax = plt.ylim()
plt.ylim(ymax, ymin)
plt.show() #prints test section
"""
"""
#defining the test data sets
test1=3419*np.ones((50,50)) #should not be able to find anything
test2=np.copy(test1)
test2[20][30] = 50000 #test2 brightest pixel is at (20,30)
test2[20][38] = 30000
"""

sigma_max=3 #threshold number of standard deviations that the pixel value needs to be above the mean noise
apt_size = 12  #diameter of aperture is 12 pixels, 3"
ann_size = 5 # difference in radii of the annulus circles

def find_max(data_set):
    """
    returns array of indices of the max pixel value in the data set
    """
    if data_set.max() >= 3419+sigma_max*12:
        loc_array = np.where(data_set==data_set.max()) #np.where returns two arrays, each with an index in them
        if len(loc_array)>2:
            return "Multiple max pixels"
        else:
            return np.array([int(loc_array[0]), int(loc_array[1])]) 
    else:
        return False #if there is no source with brightness above the background threshold


def sqr_apt_flux(data_set):
    """
    adds pixel values within fixed distance from the brightest pixel in the source in the shape of a square
    """
    find_max(data_set)
    
    #array slices indices
    start_index_y = find_max(data_set)[0]-int(0.5*apt_size)
    end_index_y = find_max(data_set)[0]+int(0.5*apt_size+1)
    start_index_x = find_max(data_set)[1]-int(0.5*apt_size)
    end_index_x = find_max(data_set)[1]+int(0.5*apt_size+1)
    apt_data = data_set[start_index_y:end_index_y,start_index_x:end_index_x] #slice the data array into the aperture square
    flux = np.sum(apt_data) #adds all the pixel values in the aperture square
    return flux


def circ_mask(data_set, centre, radius):
    """
    creates a circular mask of diameter apt_size around a given centre
    """
    #centre=find_max(data_set)
    indexy,indexx = np.ogrid[:len(data_set),:len(data_set[1])]
    r = np.sqrt((indexx - centre[1])**2 + (indexy-centre[0])**2)  #r is the distance between each pixel and the max value pixel
    mask = r > radius #creates mask which is False for pixels which are within the aperture 
    return mask


def circ_apt_flux(data_set,centre):
    """
    adds pixel values within fixed distance from the brightest pixel in the source in the shape of a circle. 
    returns the total flux and the number of pixels inside the aperture.
    """
    #centre=find_max(data_set)
    #print(centre)
    #centre = np.array([y,x])
    apt_mask=circ_mask(data_set, centre, apt_size*0.5)
    masked_data = np.ma.array(data_set.tolist(), mask=apt_mask) #masks data to a circular aperture about the max pixel
    flux = masked_data.sum()
    N=np.count_nonzero(masked_data) - np.sum(apt_mask)
    return flux, N


def ann_ref(data_set, centre):
    """
    finds the mean flux in counts/pixel in an annular reference about the brightest point of a source
    """
    #centre=find_max(data_set)
    apt_mask = circ_mask(data_set, centre, 0.5*apt_size)
    sources_mask = data_set>=(3419+sigma_max*12) #masks pixels above the background range
    ann_circ_mask = circ_mask(data_set, centre, 0.5*apt_size+ann_size)
    ann_mask1 = np.logical_or(ann_circ_mask,apt_mask) 
    ann_mask = np.logical_or(ann_mask1,sources_mask) #annulus mask is True outside outer circle and inside inner circle. False in between.
    masked_ann_data = np.ma.array(data_set.tolist(), mask=ann_mask)
    mean = np.mean(masked_ann_data)
    return mean

#print(ann_ref(test2))

def flux(data_set, centre):
    """
    returns the source flux 
    """
    flux, N = circ_apt_flux(data_set, centre)
    return (flux - N*ann_ref(data_set, centre))

