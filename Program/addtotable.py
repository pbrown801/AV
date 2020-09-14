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

inFile = '../Brown_Walker_table_1_SN.tex'

inTable = pd.read_csv(inFile,header=None,delimiter=" & ",skipinitialspace=True,comment="#")
ra = Angle(inTable.iloc[:,1])
dec = Angle(inTable.iloc[:,2])

sourceCoords = SkyCoord(ra,dec,frame='fk5')


TableAVs = [None]*len(ra)
endlines = ["\\"]*len(ra)

for i in range(0,len(sourceCoords)):
	TableAVs[i] = getAV(sourceCoords[i])

inTable['original']=TableAVs  
#

final_columns=np.stack((inTable.iloc[:,0],inTable.iloc[:,1],inTable.iloc[:,2],inTable.iloc[:,3],inTable.iloc[:,7],inTable.iloc[:,4],inTable.iloc[:,5], inTabl.iloc[:,6]),axis=1)

np.savetxt("Brown_Walker_table_1_newSN.dat", final_columns, delimiter=" & ",fmt='%s')

print('Done!')