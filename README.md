# AstroImageProcess
Identifies and calculates the flux of objects in an image from a FITS file. Uses Python 3.9.0 requiring numpy, matplotlib, scipy and astropy.

A1_mosaic.fits - FITS file for image used.
detect_test.py - Carries out a test on a data set for masking unwanted pixels and catalogueing objects.
flux_calibration.py - A test for local background and flux measurement.
global_test.py - A series of tests for the global detection of galaxies.
header.txt - A copy of the FITS header in a readable format.
hist.py - Fits a Gaussian profile to the background of the image.
image_anal_ann.py - Plots the logN vs m function for a range of annulus sizes.
image_anal_app.py - Plots the logN vs m function for a range of aperture sizes.
image_anal.py - Uses the points csv file and the photometry functions to construct the catalogue and plots a logN vs m graph with a linear curve fit.
img.py - Displays the image for checks by eye.
masking.py - Masks image to indicate prescence of objects.
photometry.py - Contains the functions find_max, circ_mask, sqr_apt_flux, circ_apt_flux, ann_ref, flux. These are necessary for the local photometry analysis of each object.
profile_gauss.py - Creates a Gaussian profile and fits a Sersic profile to the intensity.
profile_hist.py - Plots a histogram of the Sersic indices calculated.
profile_test.py - Calculates the Sersic index for every point identified.
profile.py - Contains functions for finding the intensity at a range of radii and the Sersic index of an object.
sersic_indiv.py - Fits a Sersic profile to an individual object.
test_photometry.py - Tests the photometry functions on a test data set with one bright pixel at x=30, y=20.
