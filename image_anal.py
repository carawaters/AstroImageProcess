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


#find these for every point

for k in range(3,16,2):
    ann_size= k
    apt_size = 12

    tot_flux=[] #total flux through circular aperture
    err_tot_flux=[] #error in the total flux is the square root of it due to Poisson distribution
    source_flux=[] #flux due to source through circular aperture
    loc_backgrnd=[] #background in annular reference around source
    mag=[] #apparent magnitude of source
    index_x=[] #x index of centre of source
    index_y=[] #y index of centre of source

    for i in range(0,len(pointsx)):
        x=int(pointsx[i])
        y=int(pointsy[i])
        #print(data[y][x])

        if x > 25.0 and y > 25.0 and y<len(data)-25.0 and x<len(data[0])-25.0:
        #slice a section of the total image around each source to carry out flux analysis. For this, the point cannot lie too close to the edge.

            index_x.append(x)
            index_y.append(y)
        
            data_set = data[int(y-25):int(y+25),int(x-25):int(x+25)] 
            centre=np.array([25,25]) #the centre is fixed due to the sliced section
            i_tot_flux, N = circ_apt_flux(data_set,centre, apt_size)
            tot_flux.append(i_tot_flux) #find individual total flux
            i_err_tot_flux = np.sqrt(i_tot_flux)
            err_tot_flux.append(i_err_tot_flux) #individual error in total flux
            i_loc_backgrnd=ann_ref(data_set, centre, apt_size, ann_size)
            loc_backgrnd.append(i_loc_backgrnd) #individual background 
            i_source_flux = flux(data_set, centre, apt_size, ann_size)
            source_flux.append(i_source_flux) #individual source flux
            i_mag = header["MAGZPT"] -2.5*np.log10(i_source_flux)
            mag.append(i_mag) #individual apparent magnitude

    catalogue_anal = [index_x, index_y, tot_flux, err_tot_flux, source_flux, loc_backgrnd, mag]
    with open("catalogue_anal.csv","w") as f:
        wr = csv.writer(f)
        wr.writerows(catalogue_anal) #this saves a csv file with each row being one of the lists inside the catalogue


    N = []
    for j in range(0,2500):
        m_cum = [x for x in mag if x <= j*0.01]
        N.append(len(m_cum))

    m = np.arange(0,25, 0.01)
    m2= np.arange(13.5,18,0.1)
    N=np.array(N)
    plt.plot(m,np.log10(N), label = "Ann size = "+str(ann_size))





plt.xlabel("m")
plt.ylabel("log(N)")
plt.ylim(0,3.5)
plt.xlim(7.5,25)
plt.legend()
plt.grid()
plt.show()
