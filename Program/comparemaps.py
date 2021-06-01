from __future__ import print_function

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import astropy.units as units
from astropy.coordinates import SkyCoord
from astropy.coordinates import Angle
from astroquery.irsa_dust import IrsaDust

import healpy as hp
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from dustmaps.sfd import SFDQuery
from dustmaps.planck import PlanckQuery
from dustmaps.bayestar import BayestarQuery

#import getAVbest2
#import getAVbest
import dustmaps.planck
#dustmaps.planck.fetch()
	

inFile = 'Brown_Walker_table_1.dat'
inTable = pd.read_csv(inFile,header=None,delimiter=' ')
names = inTable.iloc[:,0]
allra = inTable.iloc[:,1]
alldec = inTable.iloc[:,2]
distances = inTable.iloc[:,3]
cardinalAV = inTable.iloc[:,4]
cardinalAVspread = inTable.iloc[:,5]
n=len(inTable.index)
    
print(cardinalAV)

SF2011AVs = [None]*n
SFDqueryAVs = [None]*n
BW2021AVs = [None]*n
BW20212AVs = [None]*n
PlanckAVs = [None]*n
HIAVs = [None]*n
index = [i for i in range(n)]


for j in index:


    ra0, dec0 = allra[j], alldec[j]
    
    sourceCoords = SkyCoord(ra0,dec0,frame='icrs')
    print("sourceCoords ", sourceCoords)

    sfd = SFDQuery()
    # this conversion puts Av on the Schlafly system
    Av_sfd = 2.742 * sfd(sourceCoords)
    print("av_sfd good")
    planck = PlanckQuery()
    Av_planck = 3.1 * planck(sourceCoords)
    print("av_planck good")

    AVtable = IrsaDust.get_extinction_table(sourceCoords,show_progress = False)
    AV=AVtable['A_SandF'][2]
    print("av_sandf good")

    SF2011AVs[j] = AV
    SFDqueryAVs[j] = Av_sfd
    # BW2021AVs[j],err,source = getAVbest(SourceCoords)
    # BW20212AVs[j],err,source = getAVbest2(SourceCoords)
    PlanckAVs[j] = Av_planck

    # https://nbviewer.jupyter.org/github/DanielLenz/ebv_tools/blob/master/examples.ipynb
    ebv_map = hp.read_map('/Users/pbrown/Desktop/SN/github/ebv_tools/ebv_lhd.hpx.fits', verbose=False)
    nside = hp.get_nside(ebv_map)
    npix = hp.nside2npix(nside)
    ordering = 'ring'

    s_gal = sourceCoords.galactic
    glon = s_gal.l.value
    glat = s_gal.b.value
    pix = hp.ang2pix(nside, glon, glat, lonlat=True)
    
    # get reddening for these pixels
    ebv_los = ebv_map[pix]
    # the conversion puts it on the schlafley system
    HIAVs[j] = ebv_los*2.742
    print("av_hi good")

    imagename=names[j]+'_radeccomparison.png'

    ra0 = Angle(ra0)
    dec0 = Angle(dec0)

    print(ra0, dec0)

    ra = np.arange(ra0.degree - 2., ra0.degree + 2., 0.05)
    dec = np.arange(dec0.degree - 2., dec0.degree + 2., 0.05)
    ra, dec = np.meshgrid(ra, dec)
    coords = SkyCoord(ra*units.deg, dec*units.deg, frame='icrs')



    sfd = SFDQuery()
    # this conversion puts Av on the Schlafly system
    Av_sfd = 2.742 * sfd(coords)
    
    planck = PlanckQuery()
    Av_planck = 3.1 * planck(coords)

#bayestar = BayestarQuery(max_samples=1)
#Av_bayestar = 2.742 * bayestar(coords)

    fig = plt.figure(figsize=(8,4), dpi=150)

    for k,(Av,title) in enumerate([(Av_sfd, 'SFD'),
                               (Av_planck, 'Planck')]):


        ax = fig.add_subplot(1,2,k+1)
        ax.imshow(
         np.sqrt(Av)[::,::-1],
         vmin=0.,
         vmax=0.5,
         origin='lower',
         interpolation='nearest',
         cmap='binary',
         aspect='equal'
        )
        ax.axis('off')
        ax.set_title(title)

    fig.subplots_adjust(wspace=0., hspace=0.)
    plt.savefig(imagename, dpi=150)

x=cardinalAV[0:n]

for j in index:
    print(names[j], x[j], SF2011AVs[j], SFDqueryAVs[j], PlanckAVs[j], HIAVs[j])

plt.clf()
fig = plt.figure(figsize=(4,4), dpi=150)
plt.plot(x,SF2011AVs, color = '#00429d', marker = "o", linestyle='none', label = "SF2011")
plt.plot(x,SFDqueryAVs, color = '#73a2c6', marker = ".", linestyle='none',  label = "SFDquery")
plt.plot(x,PlanckAVs, color = '#f4777f', marker = "x",  linestyle='none', label = "Planck")
plt.plot(x,HIAVs, color = '#93003a', marker = "H",  linestyle='none', label = "HI")
#plt.axvline(x=majAxis[j])
plt.xlabel("Annular A$_V$")
plt.ylabel("A$_V$")
plt.legend(loc='bottom right', shadow=True)
#    plt.suptitle("A$_V$ Values by Arcminute")
ax.set_aspect('equal', adjustable='box')
ax.set_xscale('log')
plt.xlim(0.01,3)
ax.set_yscale('log')
plt.ylim(0.01,3)
plt.savefig('AVcomp.png', dpi=150)



