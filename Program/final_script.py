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

for i in compCoords:
	# print(type(i.separation(sourceCoords)))
	separations = i.separation(sourceCoords).arcminute
	within = np.less(separations,inTabl.iloc[:,3])
	print(within)
	correctedAVs = np.where(within,inTabl.iloc[:,4],np.nan)
	print(correctedAVs)
	# if separations < inTabl.iloc[:,4]:
	# 	separations = True
	# print(separations)
	# print('-----\n')



# name = tabl.iloc[:,0]
# rad = tabl.iloc[:,1]
# dec = tabl.iloc[:,2]
# radius = tabl.iloc[:,3]
# av = tabl.iloc[:,4]
# err = tabl.iloc[:,5]

