import numpy as np
from astropy.io import fits
import csv
hdulist = fits.open('A1_mosaic.fits')


header = hdulist[0].header
data_raw = hdulist[0].data
data = data_raw[2500:3500,1000:2000]

hdulist.close()

from photometry import circ_apt_flux,ann_ref,flux
import matplotlib.pyplot as plt

pointsx, pointsy=np.loadtxt("catalog.csv", delimiter=",", unpack = True)
points=[pointsx,pointsy]

#lists which will contain the values in the catalogue
tot_flux=[] #total flux through circular aperture
err_tot_flux=[] #error in the total flux is the square root of it due to Poisson distribution
source_flux=[] #flux due to source through circular aperture
loc_backgrnd=[] #background in annular reference around source
mag=[] #apparent magnitude of source
index_x=[] #x index of centre of source
index_y=[] #y index of centre of source

#find these for every point

#for i in range(10,20):

for i in range(0,len(pointsx)):
    x=int(pointsx[i])
    y=int(pointsy[i])
    #print(data[y][x])

    if x > 15.0 and y > 15.0 and y<len(data)-15.0 and x<len(data[0])-15.0:
    #slice a section of the total image around each source to carry out flux analysis. For this, the point cannot lie too close to the edge.

        index_x.append(x)
        index_y.append(y)
    
        data_set = data[int(y-15):int(y+16),int(x-15):int(x+16)] 
        centre=np.array([14,14]) #the centre is fixed due to the sliced section
        i_tot_flux, N = circ_apt_flux(data_set,centre)
        tot_flux.append(i_tot_flux) #find individual total flux
        i_err_tot_flux = np.sqrt(i_tot_flux)
        err_tot_flux.append(i_err_tot_flux) #individual error in total flux
        i_loc_backgrnd=ann_ref(data_set, centre)
        loc_backgrnd.append(i_loc_backgrnd) #individual background 
        i_source_flux = flux(data_set, centre)
        source_flux.append(i_source_flux) #individual source flux
        i_mag = header["MAGZPT"] -2.5*np.log10(i_source_flux)
        mag.append(i_mag) #individual apparent magnitude



catalogue_anal = [index_x, index_y, tot_flux, err_tot_flux, source_flux, loc_backgrnd, mag]
with open("catalogue_anal.csv","w") as f:
    wr = csv.writer(f)
    wr.writerows(catalogue_anal) #this saves a csv file with each row being one of the lists inside the catalogue


N = []
for j in range(1000,2500):
    m_cum = [x for x in mag if x <= j*0.01]
    N.append(len(m_cum))

m = np.arange(10,25, 0.01)
m2= np.arange(13.5,18,0.1)
N=np.array(N)
def func(x):
    return 0.6*x - 7.5
plt.plot(m,np.log10(N), label = "Data")
plt.plot(m2,func(m2), label="log(N) = 0.6m - 7.5")
plt.xlabel("m")
plt.ylabel("log(N)")
plt.legend()
plt.grid()
plt.show()
