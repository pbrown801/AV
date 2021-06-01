

def getAV(coord):
    from astroquery.irsa_dust import IrsaDust
    from astropy.coordinates import Angle,ICRS,SkyCoord
#    print(coord)
#    C = SkyCoord(coord, frame = 'icrs')
#    print(C)
    table = IrsaDust.get_extinction_table(coord,show_progress = False)
#    print(table['A_SandF'][2])
    return (table['A_SandF'][2])


def annulusmedian(distance,ra_central,dec_central):
    from astropy.coordinates import Angle,ICRS,SkyCoord
    import numpy as np
    import math
    from astropy import units as u
    from astropy import coordinates
#    print('starting annulusmedian ', distance, ra_central, dec_central)
#    ra='12h00m00.0s'
#    dec='00d00m00.00s'
#    distance=60.0    
    degreedistance=distance/60.0

    """
        Gets 360 coordinates a specified distance away from the center of the galaxy
        Inputs:
            distance: distance in arcminutes
            ra_central: right ascension component of the coordinate
            dec_central: declination component of the coordinate
        Outputs:
            ring_coords: list of coordinates *distance* arcminutes away from the center of the specified galaxy

    """

    ring_coords = [None]*360 
    directions = [i for i in range(360)]
    AVloop = [i for i in range(360)]

#    print('just before skycoord ',ra_central, ' ', dec_central)

    inputcoord=SkyCoord(ra_central,dec_central,frame='fk5')
#    print(inputcoord)

    for direction in directions:
#        print(direction)
        newdec=inputcoord.dec+Angle(degreedistance*math.cos(direction*2.0*3.14159/360.0),unit=u.degree)
#        print(newdec)
        newra=inputcoord.ra+Angle(math.cos(newdec.value*2.0*3.14159/360.0)*degreedistance*math.sin(direction*2.0*3.14159/360.0),u.degree)
#        print(newra)
         
        ring_coords[direction] = SkyCoord(ra=newra, dec=newdec)
#        print(ring_coords)
#    print(ring_coords)
        AVloop[direction]=getAV(ring_coords[direction])

    AVmedian=np.median(AVloop)
    AVstddev=np.std(AVloop)

    return AVmedian, AVstddev; #performs transformation of initial coordinate into cardinal coordinates


def updatetable():
    print("updating the table")
    import math
    import sys
    from astropy import units as u
    from astropy import coordinates
    from astropy.coordinates import Angle,ICRS,SkyCoord
    import numpy as np
    import pandas as pd

    inFile = 'Brown_Walker_table_1.dat'
    inTable = pd.read_csv(inFile,header=None,delimiter=' ')
    names = inTable.iloc[:,0]
    ra = Angle(inTable.iloc[:,1])
    dec = Angle(inTable.iloc[:,2])
    distances = inTable.iloc[:,3]
    cardinalAV = inTable.iloc[:,4]
    cardinalAVspread = inTable.iloc[:,5]
    sourceCoords = SkyCoord(ra,dec,frame='fk5')


    n=len(inTable.index)
    
    medianAVs = [None]*n
    stddevAVs = [None]*n
    index = [i for i in range(n)]


    for j in index:
        i=j+50
        coords=sourceCoords[i] 
#        print('i')
#        print(coords)
#        print(distances[i])
#        print(cardinalAV[i])
        med, stddev=annulusmedian(distances[i],ra[i], dec[i])

        medianAVs[i]=med
        stddevAVs[i]=stddev
        print(cardinalAV[i], cardinalAVspread[i], med, stddev)


# this didn't work, so the screen output was copied into the table    np.savetxt("Brown_Walker_table_1_rev1.dat", inTable.iloc[:,0],inTable.iloc[:,1],inTable.iloc[:,2],inTable.iloc[:,3], medianAVs, stddevAVs, delimiter=" ",fmt='%s')


if __name__ == "__main__": 
    updatetable() 
