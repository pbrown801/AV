import time
print("begin ", time.time())
from astropy import units as u
print("after import u", time.time())
from astropy import coordinates
print("after import coordinates", time.time())
#from astroquery.ned import Ned
#print("after import ned", time.time())
#from astroquery.irsa_dust import IrsaDust
#print("after import dust", time.time())
from astropy.coordinates import Angle,ICRS,SkyCoord
print("after import angle", time.time())
from astropy.coordinates.name_resolve import NameResolveError
print("after import name resolve", time.time())
from astropy.utils.data import download_file
print("after import download", time.time())
from astropy.io import fits
print("after import fits", time.time())
from astropy.table import Table
print("after import table", time.time())
from astropy.table import Column
print("after import column", time.time())
import matplotlib
matplotlib.__version__
print("after import matplotlib", time.time())
import csv
print("after import csv", time.time())
import time
print("after import time", time.time())

def coord_breakup(coord):
    """
        Breaks up a coordinate into its components
    """
    ra = Angle(coord.ra.hour,unit = u.hour)
    dec = coord.dec
    return(ra,dec)


def get_coords(gals):
    """
        Takes list of galaxies and looks up their coordinates by name.
        If no name found: warn, skip, remove galaxy from list

        Returns:
            gals: list of galaxies minus those that weren't found
            start_coord: list of coordinates corresponding to center of galaxies in 'gals'
        This version removes the status bar due to tkinter issues

    """
    start_coord = []
    ra_list = []
    dec_list = []
    for i in gals[:]: #gets all valid galaxies
        try:
            tempCoord = SkyCoord.from_name(i, frame = 'icrs')
            start_coord.append(coordinates.SkyCoord(tempCoord))
            ra_list.append(tempCoord.ra)
            dec_list.append(tempCoord.dec)

        except NameResolveError:
            print('\nSkipping',i,'because it couldn\'t be found.')
            gals.remove(i)
    return(gals,ra_list,dec_list)



print("before input ", time.time())
input_file='../bright_gals_comments.csv'
print("after input ", time.time())
gals = []
galaxy_list = []
comments_list = []
AVnew_list = []
AVerr_list = []
AVrad_list = []
morecomments_list = []
with open(input_file) as input:
    reader=csv.reader(input,delimiter=',')
    for row in reader:
        galname,comment,AVnew,AVerr,AVrad,morecomments=row[0:6]
        galaxy_list.append(galname.replace(" ", ""))
        AVnew_list.append(AVnew)
        AVerr_list.append(AVerr)
        AVrad_list.append(AVrad)
        comments_list.append(comment)
        morecomments_list.append(morecomments)

print("after reading in ", time.time())

gals, ra_list, dec_list = get_coords(galaxy_list)

ra_list_new = []
dec_list_new = []

for i, ra in enumerate(ra_list):
    ra_list_new.append(ra.to_string(unit=u.hour))
    if AVnew_list[i] != '':
        print(galaxy_list[i],ra_list_new[i], dec_list[i], AVrad_list[i], AVnew_list[i], AVerr_list[i])



print("after coordinates ", time.time())

for i, ra in enumerate(ra_list):
    if AVnew_list[i] != '':
        print(galaxy_list[i], ' & ', ra_list_new[i],  ' & ', dec_list[i],  ' & ', AVrad_list[i],  ' & ', AVnew_list[i],  ' & ', AVerr_list[i]) ' \\ ', 


