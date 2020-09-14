#!/usr/bin/env python3

from astropy.coordinates import SkyCoord
from astropy.coordinates import Angle, Latitude, Longitude
from astroquery.irsa_dust import IrsaDust

import astropy.units as u
import pandas as pd
import numpy as np
import math
#import argparse

import sys

#parser = argparse.ArgumentParser(description='Process coordinates for AV observation.')

#parser.add_argument('input', metavar='input', type=str, nargs=1, help='A file to process.')

#args = parser.parse_args()

#testra = args.input[1]
#testdec = args.input[2]
#testra = sys.argv[1]
#testdec = sys.argv[2]
#testra = '17h04m50.999s'
#testdec = '12d55m29.64s'
input = sys.argv[1]
print(input)
#input = args.input[0]
#print(input)
#testCoords = SkyCoord(testra,testdec,frame='fk5')
testCoords = SkyCoord(input,frame='fk5')
#newVals = [None]*len(testCoords)
#newAVs = [None]*len(testCoords)
#newAVerrs = [None]*len(testCoords)


AVtable = IrsaDust.get_extinction_table(testCoords,show_progress = False)
AV=mapAVtable['A_SandF'][2]
AVerr = mapAV*0.1
source = 'Schlafly'



print('\n-----\nReading input files...')
inFile = 'Brown_Walker_table_1.dat'
inTabl = pd.read_csv(inFile,header=None,delimiter=' ')
ra = Angle(inTabl.iloc[:,1])
dec = Angle(inTabl.iloc[:,2])

sourceCoords = SkyCoord(ra,dec,frame='fk5')


print('Calculating separation and replacing values...')

separations = testCoords.separation(sourceCoords).arcminute
within = np.less(separations,inTabl.iloc[:,3])
correctedAV = np.where(within,inTabl.iloc[:,4],None) #get calculated val

if correctedAV :
    AV = next((item for item in correctedAV if item is not None),None)
    correctedAVerr = np.where(within,inTabl.iloc[:,5],None) #get calculated val
    newAVerr = next((item for item in correctedAVerr if item is not None),None)
    AVerr = math.sqrt((newAVerr)**2+(newAV*0.1)**2)
    source = ['Brown & Walker']



#compCoords = compCoords.to_string('hmsdms')
# finalVals = np.stack((compCoords,newVals,source),axis=1)

#np.savetxt("corrected_av.csv", finalVals, delimiter=",",fmt='%s')
print(newAV, newAVerr)
#return(newAV, newAVerr,source)
