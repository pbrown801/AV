from __future__ import print_function

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import astropy.units as units
from astropy.coordinates import SkyCoord
from astropy.coordinates import Angle

from dustmaps.sfd import SFDQuery
from dustmaps.planck import PlanckQuery
from dustmaps.bayestar import BayestarQuery

import dustmaps.planck
#dustmaps.planck.fetch()
	
'''
l0, b0 = (121.174405, -21.572936)
imagename='M31comparison.png'

l0, b0 = (138.320313, 68.842121)
imagename='NGC4258comparison.png'

##  Galactic coordinates for M33
l0, b0 = (133.610161, -31.330587)
imagename='M33comparison.png'

l = np.arange(l0 - 1., l0 + 1., 0.05)
b = np.arange(b0 - 1., b0 + 1., 0.05)
l, b = np.meshgrid(l, b)
coords = SkyCoord(l*units.deg, b*units.deg,
                  distance=1.*units.kpc, frame='galactic')
'''

ra0, dec0 = '12h18m57.5046s', '+47d18m14.303s'
imagename='NGC4258radeccomparison.png'

ra0 = Angle(ra0)
dec0 = Angle(dec0)

print(ra0, dec0)

ra = np.arange(ra0.degree - 2., ra0.degree + 2., 0.05)
dec = np.arange(dec0.degree - 2., dec0.degree + 2., 0.05)
ra, dec = np.meshgrid(ra, dec)
coords = SkyCoord(ra*units.deg, dec*units.deg, frame='icrs')



sfd = SFDQuery()
Av_sfd = 2.742 * sfd(coords)
print(Av_sfd)
planck = PlanckQuery()
Av_planck = 3.1 * planck(coords)

#bayestar = BayestarQuery(max_samples=1)
#Av_bayestar = 2.742 * bayestar(coords)

fig = plt.figure(figsize=(8,4), dpi=150)

for k,(Av,title) in enumerate([(Av_sfd, 'SFD'),
                               (Av_planck, 'Planck')]):
#,
#                               (Av_bayestar, 'Bayestar')

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
