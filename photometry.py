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
        if len(loc_array)>2:
            return "Multiple max pixels"
        else:
            return np.array([int(loc_array[0]), int(loc_array[1])]) 
    else:
        return False #if there is no source with brightness above the background threshold

#print(find_max(test2)) #returns array [20,30] as expected
#print(find_max(test1)) #returns False as expected
#print(test2[find_max(test2)[0]][find_max(test2)[1]]) #prints max value

def square_aperture_flux(data):
    """
    adds pixel values within fixed distance from the brightest pixel in the source in the shape of a square
    """
    find_max(data)
    apt_size = 12 #diameter of aperture is 12 pixels, 3"
    
    #array slices indices
    start_index_x = find_max(data)[0]-int(0.5*apt_size)
    end_index_x = find_max(data)[0]+int(0.5*apt_size+1)
    start_index_y = find_max(data)[1]-int(0.5*apt_size)
    end_index_y = find_max(data)[1]+int(0.5*apt_size+1)
    print(start_index_x,end_index_x,start_index_y,end_index_y)
    apt_data = data[start_index_x:end_index_x,start_index_y:end_index_y] #slice the data array into the aperture square
    flux = np.sum(apt_data) #adds all the pixel values in the aperture square
    return(flux)

print(square_aperture_flux(test2)) #returns (13*13) * 3419 +(50000-3419)= 624392 as expected
