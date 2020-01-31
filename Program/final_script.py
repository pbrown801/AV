from astropy.coordinates import SkyCoord
from astropy.coordinates import Angle, Latitude, Longitude
from astroquery.irsa_dust import IrsaDust

import astropy.units as u
import pandas as pd
import numpy as np

import argparse


#name | ra | dec | radius | uncertainty | 

def getAV(coord):
	table = IrsaDust.get_extinction_table(coord,show_progress = False)
	return (table['A_SandF'][2])

parser = argparse.ArgumentParser(description='Process coordinates for AV observation.')

parser.add_argument('input', metavar='input', type=str, nargs=1, help='A file to process.')

args = parser.parse_args()

testFile = args.input[0]


print('\n-----\nReading input files...')
inFile = 'Brown_Walker_table_1.dat'
# testFile = 'testIn.dat'

#read input table

inTabl = pd.read_csv(inFile,header=None,delimiter=' ')
ra = Angle(inTabl.iloc[:,1])
dec = Angle(inTabl.iloc[:,2])

sourceCoords = SkyCoord(ra,dec,frame='fk5')


#read comparison table

testTabl = pd.read_csv(testFile,header=None,delimiter=' ')
testRa = Angle(testTabl.iloc[:,0])
testDec = Angle(testTabl.iloc[:,1])

print('Calculating separation and replacing values...')
compCoords = SkyCoord(testRa,testDec,frame='fk5')
newVals = [None]*len(compCoords)
source = ['Walker & Brown']*len(compCoords)

for i in range(0,len(compCoords)):
	# print(type(i.separation(sourceCoords)))
	separations = compCoords[i].separation(sourceCoords).arcminute
	within = np.less(separations,inTabl.iloc[:,3])
	correctedAVs = np.where(within,inTabl.iloc[:,4],None) #get calculated val
	newVals[i] = next((item for item in correctedAVs if item is not None),None)
	if newVals[i] == None:
		newVals[i] = getAV(compCoords[i])
		source[i] = 'Schlafly'

compCoords = compCoords.to_string('hmsdms')
finalVals = np.stack((compCoords,newVals,source),axis=1)

np.savetxt("corrected_av.csv", finalVals, delimiter=",",fmt='%s')
print('Done!')