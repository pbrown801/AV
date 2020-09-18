This repository contains the programs used for investigating the contamination of the Milky Way reddening maps from the IR luminosity of nearby galaxies

The main files of concern to those interested in the results:

AV.pdf is the paper describing this work.

Brown_Walker_table_1.dat is a version of the table from that paper

getAVbest.py takes as input a set of coordinates.  If the coordinate position lies within our warning radius from the center of a contaminating galaxy, it outputs our recommended A_V value (on the Schlafly & Finkbeiner 2011 system) based on the map values a safe distance from the center, our recommended uncertainty on A_V, and the appropriate reference (our paper, Schegel et al. 1998 for the regions around LMC, SMC, and M31, and Dalcanton et al. 2009 for M82).
If the coordinates are far enough away from these positions, the value from the Schlafly & Finkbeiner 2011 recalibration of the Schlegel et al. 1998 maps is returned.

Graphs/ contains the plots of A_V versus distance for the galaxies of concern 
Pictures/ contains images of the dust reddening maps for the galaxies of concern
Program/ contains most of the programs used throughout this project, some of which are documented in more detail below.

# Galactic Data
Program/runScript.py

-Script to query IRSA database for galactic A_v Extinction values at a certain arcminute length away

-Option to graph values and fetch IR images off IRSA

-Contains error checking
 

quickdata.py:

-Script to grab various properties from NED for different galaxies

-Contains error checking


randomGal.py:

-Script to create x amount of random coordinates and pull AV values for each

-Contains error checking



All values are stored in .csv files and appropriate pictures and graphs are stored in their respective folders.

*DO NOT DELETE SUPPLIED FOLDERS*

Included is a list of packages required for the program to work. I used Anaconda to install these and recommend the same.

Created by: Tate Walker for Dr. Peter Brown at Texas A&M University, Summer 2017-Fall 2019
