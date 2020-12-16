"""
Masks image to indicate prescence of objects.
"""

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

#function to give a circular mask dependent on radius
def create_circular_mask(width, height, centre, radius):
    x, y = np.ogrid[:width, :height]

    dist_from_centre = np.sqrt((x - centre[0])**2 + (y - centre[1])**2) #find min distance to check if within radius
    mask = dist_from_centre <= radius

    return mask

def bright_mask(data, thresh, val_min, noise_mean, noise_std, width, height):
    #set up overall mask
    bright_points = data[data >= thresh]
    indices = np.nonzero(data >= thresh)
    current_mask = np.array(data <= val_min, dtype=bool)
    print(len(bright_points))

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
        print(i)
    return current_mask

def catalogue(data, current_mask, radius, width, height, fname):
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