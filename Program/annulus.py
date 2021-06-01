moved into utilities  def annulus(distance,ra,dec):
#def annulus():
    import math
    import sys
    from astropy import units as u
    from astropy import coordinates
    from astropy.coordinates import Angle,ICRS,SkyCoord

    
#    ra='12h00m00.0s'
#    dec='00d00m00.00s'
#    distance=60.0    
    degreedistance=distance/60.0


    """
        Gets 360 coordinates a specified distance away from the center of the galaxy
        Inputs:
            distance: distance in arcminutes
            ra: right ascension component of the coordinate
            dec: declination component of the coordinate
        Outputs:
            ring_coords: list of coordinates *distance* arcminutes away from the center of the specified galaxy

    """

    ring_coords = [None]*360 
    directions = [i for i in range(360)]
#    directions = [0, 90, 180, 270, 360]
    inputcoord=SkyCoord(ra+' '+dec)
#    print(inputcoord)

    for direction in directions:
#        print(direction)
        newdec=inputcoord.dec+Angle(degreedistance*math.cos(direction*2.0*3.14159/360.0),unit=u.degree)
#        print(newdec)
        newra=inputcoord.ra+Angle(math.cos(newdec.value*2.0*3.14159/360.0)*degreedistance*math.sin(direction*2.0*3.14159/360.0),u.degree)
#        print(newra)

        ring_coords[direction] = SkyCoord(ra=newra, dec=newdec)

#    print(ring_coords)


    return ring_coords; #performs transformation of initial coordinate into cardinal coordinates

