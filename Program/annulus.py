def annulus(distance,ra,dec):
    import math
    import sys
    from astropy import units as u
    from astropy import coordinates
    from astropy.coordinates import Angle,ICRS,SkyCoord

    print('does this work?')

    """
        Gets 360 coordinates a specified distance away from the center of the galaxy
        Inputs:
            distance: distance in arcminutes
            ra: right ascension component of the coordinate
            dec: declination component of the coordinate
        Outputs:
            ring_coords: list of coordinates *distance* arcminutes away from the center of the specified galaxy

    #angle is from astropy.coordinates

    """

    ring_coords = [None]*360 
    directions = [i for i in range(360)]
#    directions = [0, 90, 180, 270, 360]
    coord=SkyCoord(ra+' '+dec)
    print(coord)

    for direction in directions:
        print(direction)
        decli = coord.dec.arcminute+distance*math.cos(direction*2.0*3.14159/360.0)
        #print(math.cos(direction*2.0*3.14159/360.0))
        print(decli)
        decl = Angle(decli,u.arcminute)
        decl = Angle(decl.to_string(unit=u.degree),u.degree)
        coord = SkyCoord(ra=coord.ra, dec=decl)
        #print(coord)
        # converting from arcminutes into right ascension seconds
        # 24 h x 60 m/h x 60 s/m = 86400 sec
        # 360 deg x 60 arcmin/deg x 60 arsec/arcmin = 1296000 arcsec
        # in on arcminute = 60 arcsec x 86400 / 1296000 
        ds = distance*4*math.sin(direction*2*3.14159/360.0)
        ds/=math.cos(math.radians(coord.dec.degree))
        h = coord.ra.hms.h
        m = coord.ra.hms.m
        s = coord.ra.hms.s+ds
        (s,m,h) = timeFix(s,m,h) #keep time within allowed range
    
        rad = Angle((h,m,s), unit = u.hour)
        rad = Angle(rad.to_string(unit=u.hour),u.hour)
        #print(SkyCoord(ra=rad, dec=decl))
        ring_coords[direction] = SkyCoord(ra=rad, dec=decl)

#    print(ring_coords)


    return ring_coords; #performs transformation of initial coordinate into cardinal coordinates

