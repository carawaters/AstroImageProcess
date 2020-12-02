"""
finds the brightest pixel in various test data sets of 50x50 pixels and sums the pixel values within an aperture of 12 pixels
"""
import numpy as np

sigma_max=4 #threshold number of standard deviations that the pixel value needs to be above the mean noise

#defining the test data sets
test1=3419*np.ones((50,50)) #should not be able to find anything
test2=np.copy(test1)
test2[20][30] = 50000 #test2 brightest pixel is at (20,30)

def find_max(data):
    """
    returns array of indices of the max pixel value in the data set
    """
    if data.max() >= 3419+sigma_max*12:
        loc_array = np.where(data==data.max()) #np.where returns two arrays, each with an index in them
        return np.array([int(loc_array[0]), int(loc_array[1])]) 
    else:
        return False #if there is no source with brightness above the background threshold

print(find_max(test2)) #returns array [20,20] as expected
print(find_max(test1)) #returns False as expected


