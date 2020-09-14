from utilities import *
from astroquery.irsa_dust import IrsaDust
from astropy.coordinates import Angle,ICRS,SkyCoord
from astropy.coordinates.name_resolve import NameResolveError
c = SkyCoord('00h42m44.5s','+41d16m09s')
print(IrsaDust.get_query_table(c,show_progress = False,section='ebv'))
from dustmaps.sfd import SFDQuery