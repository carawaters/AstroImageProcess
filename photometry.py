"""
Maike Lenz, 07/12/20
contains the functions find_max, circ_mask, sqr_apt_flux, circ_apt_flux, ann_ref, flux
These are necessary for the local photometry analysis of each object
"""
import numpy as np
from astropy.io import fits
hdulist = fits.open('A1_mosaic.fits')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

header = hdulist[0].header
data = hdulist[0].data

hdulist.close()
data_small = data[1430:1500,1180:1230]

sigma_max=3 #threshold number of standard deviations that the pixel value needs to be above the mean noise

def find_max(data_set):
    """
    returns array of indices of the max pixel value in the data set
    input: data set
    output: array with the y coordinate and x coordinate of the maximum brightness pixel
    """
    if data_set.max() >= 3419+sigma_max*12:
        loc_array = np.where(data_set==data_set.max()) #np.where returns two arrays, each with an index in them
        return np.array([int(loc_array[0][0]), int(loc_array[1][0])]) 
    else:
        return False #if there is no source with brightness above the background threshold


def sqr_apt_flux(data_set, apt_size):
    """
    adds pixel values within fixed distance from the brightest pixel in the source in the shape of a square
    input: data set, square aperture side length
    output: total flux through aperture
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
    creates a circular mask of a given radius around a given centre and finds total flux. 
    The mask is false within the aperture and true outside.
    input: data set, central pixel coordinates, radius of the mask
    output: mask
    """
    indexy,indexx = np.ogrid[:len(data_set),:len(data_set[1])]
    r = np.sqrt((indexx - centre[1])**2 + (indexy-centre[0])**2)  #r is the distance between each pixel and the max value pixel
    mask = r > radius #creates mask which is False for pixels which are within the aperture 
    return mask


def circ_apt_flux(data_set,centre, apt_size):
    """
    Adds pixel values within fixed distance from the brightest pixel in the source in the shape of a circle. 
    input: data set, central pixel coordinates, aperture diameter
    output: total flux through aperture, N=number of pixels in aperture
    """
    apt_mask=circ_mask(data_set, centre, apt_size*0.5) #create circular mask with radius half the aperture size
    masked_data = np.ma.array(data_set.tolist(), mask=apt_mask) #masks data to a circular aperture about the max pixel
    flux = masked_data.sum()
    N=len(data_set)*len(data_set[0]) - np.sum(apt_mask)
    return flux, N


def ann_ref(data_set, centre, apt_size, ann_size):
    """
    finds the mean flux in counts/pixel in an annular reference about the brightest point of a source.
    input: data set, central pixel coordinates, aperture diameter, annulus size
    output: mean background in annulus, Na=number of pixels in annulus not counting other sources.
    """
    #centre=find_max(data_set)
    apt_mask = ~circ_mask(data_set, centre, 0.5*apt_size) #true inside aperture, false everywhere else
    sources_mask = data_set>=(3419+sigma_max*12) #masks pixels above the background range to exclude sources
    ann_circ_mask = circ_mask(data_set, centre, 0.5*apt_size+ann_size) #true outside outer circle
    ann_mask1 = np.logical_or(ann_circ_mask,apt_mask) 
    ann_mask = np.logical_or(ann_mask1,sources_mask) #annulus mask is True outside outer circle and inside inner circle. False in between.
    masked_ann_data = np.ma.array(data_set.tolist(), mask=ann_mask)
    mean = np.mean(masked_ann_data)
    Na = len(data_set)*len(data_set[0]) - np.sum(ann_mask) #numberof pixels contributing to annular reference
    return mean,Na

def flux(data_set, centre, apt_size, ann_size):
    """
    returns the source flux 
    input: data set, centre, aperture diameter, annulus size
    output: source flux
    """
    flux, N = circ_apt_flux(data_set, centre, apt_size) #N is number of pixels in aperture
    loc_backgrnd,Na=ann_ref(data_set, centre, apt_size, ann_size)
    return (flux - N*loc_backgrnd) #subtract the total background contribution in the aperture
