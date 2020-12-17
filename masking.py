"""
Masks image to indicate prescence of objects.
Author: Cara Waters
Date: 30/11/20
"""
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

#function to give a circular mask dependent on radius
def create_circular_mask(width, height, centre, radius):
    """
    Creates a circular mask around a point.
    Inputs: width = width of data set (int), height = height of data set (int), centre = central point (list or tuple length 2),
            radius = radius of mask to be produced (int)
    Ouput: mask = boolean 2d numpy array of mask where True = unincluded
    """
    x, y = np.ogrid[:width, :height]

    dist_from_centre = np.sqrt((x - centre[0])**2 + (y - centre[1])**2) #find min distance to check if within radius
    mask = dist_from_centre <= radius

    return mask

def bright_mask(data, thresh, val_min, noise_mean, noise_std, width, height):
    """
    Masks out bright bleeding objects and adds this mask to the original mask
    Inputs: data = data set (2d numpy array), thresh = upper threshold for bright object pixels (int),
            val_min = lower noise limit (int), noise_mean = mean noise value (int), noise_std = noise standard deviation (int),
            width = width of data set (int), height = height of data set (int)
    Output: 2d boolean numpy array of new mask where True = unincluded
    """
    #set up overall mask
    bright_points = data[data >= thresh]
    indices = np.nonzero(data >= thresh)
    current_mask = np.array(data <= val_min, dtype=bool)

    bright_min = noise_mean + 2.5 * noise_std

    #find points around brightest point to exclude
    for i in range(len(bright_points)):
        coord = (indices[0][i], indices[1][i])
        brightness = data[coord[0], coord[1]]
        j = 0
        while brightness >= bright_min:
            if coord[1]+j == data.shape[0]: #check for edge cases
                break
            else:
                brightness = data[coord[0], coord[1]+j] #move diagonally for check
                j += 1
        circ = create_circular_mask(width, height, coord, j) #mask inside of bright object
        current_mask = np.logical_or(current_mask, circ)
    return current_mask

def catalogue(data, current_mask, radius, width, height, fname):
    """
    Identifies objects in image and catalogs them
    Inputs: data = data set (2d numpy array), current_mask = boolean mask to use (2d boolean numpy array),
            radius = radius expected for object to avoid identifying around (int), width = data set width (int),
            height = data set height (int), fname = file name and path for catalog produced (string)
    """
    #Points to use for catalog
    cat_pts = data[np.logical_not(current_mask)] #mask True when excluding so need to remember what we need for current use
    cat_indices = np.nonzero(np.logical_not(current_mask))
    cat_mask = current_mask

    catalog = []

    for a in range(len(cat_pts)):
        coord = (cat_indices[0][a], cat_indices[1][a])
        if cat_mask[coord] == True:
            pass
        else:
            obj_mask = create_circular_mask(width, height, coord, radius)
            obj_pts = data*obj_mask #use mask as 1/0 to give only points within range of stars
            cent = np.unravel_index(np.argmax(obj_pts), obj_pts.shape)
            if cat_mask[cent] == False:
                catalog.append((cent[1], cent[0])) #indices reversed for plotting due to indexing being reversed
            excl_mask = create_circular_mask(width, height, cent, radius)
            cat_mask = np.logical_or(cat_mask, excl_mask) #exclude points of object from being checked again

    np.savetxt(fname, catalog, delimiter=',')
    return catalog