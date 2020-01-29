from astropy.coordinates import SkyCoord
from astropy.coordinates import Angle, Latitude, Longitude
import astropy.units as u
import pandas as pd
import numpy as np



#name | ra | dec | radius | uncertainty | 


inFile = 'Brown_Walker_table_1.dat'
testFile = 'testIn.dat'

#read input table
inTabl = pd.read_csv(inFile,header=None,delimiter=' ')
ra = Angle(inTabl.iloc[:,1])
dec = Angle(inTabl.iloc[:,2])

sourceCoords = SkyCoord(ra,dec,frame='fk5')

# print(sourceCoords[0].dec.dms)

#read comparison table

testTabl = pd.read_csv(testFile,header=None,delimiter=' ')
testRa = Angle(testTabl.iloc[:,0])
testDec = Angle(testTabl.iloc[:,1])

compCoords = SkyCoord(testRa,testDec,frame='fk5')
newVals = [None]*len(compCoords)

for i in range(0,len(compCoords)):
	# print(type(i.separation(sourceCoords)))
	separations = compCoords[i].separation(sourceCoords).arcminute
	within = np.less(separations,inTabl.iloc[:,3])
	correctedAVs = np.where(within,inTabl.iloc[:,4],None)
	newVals[i] = next((item for item in correctedAVs if item is not None),None)
compCoords = compCoords.to_string('hmsdms')
finalVals = np.stack((compCoords,newVals),axis=1)

np.savetxt("corrected_av.csv", finalVals, delimiter=",",fmt='%s')