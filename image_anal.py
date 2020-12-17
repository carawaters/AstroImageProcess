"""
Maike Lenz, 09/12/2020
uses the points csv file and the photometry functions to construct the catalogue 
plots a logN vs m graph with a linear curve fit.
"""
import numpy as np
from astropy.io import fits
import csv
from scipy.optimize import curve_fit

hdulist = fits.open('A1_mosaic.fits')

header = hdulist[0].header
data_raw = hdulist[0].data
data = data_raw[5:, : ]

hdulist.close()

from photometry import circ_apt_flux,ann_ref,flux
import matplotlib.pyplot as plt

"""
making the Catalogue
"""
pointsx, pointsy=np.loadtxt("datasets/points_6std.csv", delimiter=",", unpack = True) #load points
points=[pointsx,pointsy]

ann_size= 5
apt_size = 12 #aperture diameter

#lists which will contain the values in the catalogue
tot_flux=[] #total flux through circular aperture
err_tot_flux=[] #error in the total flux is the square root of it due to Poisson distribution
source_flux=[] #flux due to source through circular aperture
loc_backgrnd=[] #background in annular reference around source
mag=[] #apparent magnitude of source
index_x=[] #x index of centre of source
index_y=[] #y index of centre of source
m_err=[]  #error in the magnitude

for i in range(0,len(pointsx)):
    """
    loops through all entries in the points csv file and appends their values to the catalogue
    """
    x=int(pointsx[i])
    y=int(pointsy[i])
    #slice a section of the total image around each source to carry out flux analysis. For this, the point cannot lie too close to the edge.
    if x>100 and y>100 and x<(len(data[0])-100) and y<(len(data)-100): #cuts off edge noise within 100 pixels
        index_y.append(y)
        index_x.append(x)
        data_set = data[int(y-15):int(y+15),int(x-15):int(x+15)]
        centre=np.array([14.0,14.0]) #the centre is fixed due to the sliced section
        i_tot_flux, N = circ_apt_flux(data_set,centre, apt_size)
        tot_flux.append(i_tot_flux) #find individual total flux
        i_err_tot_flux = np.sqrt(i_tot_flux)
        err_tot_flux.append(i_err_tot_flux) #individual error in total flux
        i_loc_backgrnd,Na=ann_ref(data_set, centre, apt_size, ann_size)
        loc_backgrnd.append(i_loc_backgrnd) #individual background 
        i_source_flux = flux(data_set, centre, apt_size, ann_size)
        source_flux.append(i_source_flux) #individual source flux
        i_mag = header["MAGZPT"] -2.5*np.log10(i_source_flux)
        mag.append(i_mag) #individual apparent magnitude
        i_m_err = np.sqrt((header["MAGZRR"])**2+(25/(4*np.log(10)**2))*((i_tot_flux+i_loc_backgrnd/Na)/(i_source_flux**2)))
        m_err.append(i_m_err) #individual error in m

catalogue = [index_x, index_y, tot_flux, err_tot_flux, source_flux, loc_backgrnd, mag, m_err]
zip(*catalogue) #converts the catalogue into the right format to be saved as a csv
np.savetxt("datasets/catalogue.csv",catalogue,fmt='%.18e')

"""
plot the cumulative log(N) vs m graph
"""
plt.figure(1)
N = []
for j in range(0,2500):
    """
    loop through the magnitudes and compute the cumulative number of objects up to a value j
    """
    m_cum = [x for x in mag if x <= j*0.01]
    N.append(len(m_cum))

m=np.arange(0,25,0.01)
N=np.array(N)

plt.plot(m,np.log10(N), label = "Aperture = "+str(apt_size))

"""
find curve fit for only the linear section of the curve
"""

def func(x,a,b):
    return a*x +b

m2_total=np.arange(12,17.01,0.01)
m2=[] #m data set for curve fit
N2=[] #N data set for curve fit
for j in range(1100,1701):
    m_cum = [x for x in mag if x <= j*0.01]
    if len(m_cum)>0:
        N2.append(len(m_cum))
        m2.append(j*0.01)
m2=np.array(m2)
N2=np.array(N2)

#find error bars
xerr=[]
m3=np.arange(12,18)
N3=[]
for j in range(12,18):
    f=10**(j-header["MAGZPT"]/(-2.5))
    err= np.sqrt((header["MAGZRR"])**2+(25/(4*np.log(10)**2))/f)
    xerr.append(err)
xerr=np.array(xerr)
N3=np.array([N2[51],N2[151],N2[251],N2[351],N2[451],N2[551]]) #integer values of m
popt,pcov=curve_fit(func,m2,np.log10(N2))
plt.plot(m2_total,func(m2_total,*popt),label="log(N) = ("+str(round(popt[0],3))+"$\pm$"+str(round(np.sqrt(pcov[0][0]),3))+")m"+" + ("+str(round(popt[1],2))+"$\pm$"+str(round(np.sqrt(pcov[1][1]),2))+")") 
plt.errorbar(m3,np.log10(N3),xerr=xerr,ls="None", capsize=5)

plt.xlabel("m")
plt.ylabel("log(N)")
plt.legend()
plt.grid()
plt.show()

