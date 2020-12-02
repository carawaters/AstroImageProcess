"""
finds the brightest pixel in various test data sets of 50x50 pixels and sums the pixel values within an aperture of 12 pixels
"""
import numpy as np

#defining the test data sets
test1=3419*sp.ones((50,50)) #should not be able to find anything
test2=test1
test2[20][30] = 50000 #test2 brightest pixel is at (20,30)


