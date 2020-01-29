# utilities.py

from astropy import units as u
from astropy import coordinates
from astroquery.ned import Ned
from astroquery.irsa_dust import IrsaDust
from astropy.coordinates import Angle,ICRS,SkyCoord
from astropy.coordinates.name_resolve import NameResolveError
from astropy.utils.data import download_file
from astropy.io import fits
from astropy.table import Table
from astropy.table import Column

import matplotlib
matplotlib.use("Tkag")
import matplotlib.pyplot as plt

import numpy as np

import math
import os.path
import sys
import itertools
import csv
import pandas as pd
import requests
import time

from progress.bar import ChargingBar,FillingCirclesBar

def csv_to_ascii(inFile,outFile):
    """
        Converts csv file to ascii file
    """
    outFile = outFile+'.txt'
    with open(outFile,'w') as output:
        with open(inFile) as csvinp:
            reader = csv.reader(csvinp,delimiter = ',')
            for row in reader:
                for col in row:
                    output.write(str(col) + ' ')
                output.write('\n')

def read_gals(input_file,desired_col=0): #remember why i need this
    """
        Reads in galaxies from different file types and parses them into a list of galaxies by name
        Returns:
            gals: list of galaxies from input file
    """
    if input_file.endswith('.xlsx'):
        df = pd.read_excel(excel_input,header = 1, parse_col = desired_col)
        print(df)
        print(df['ra'])
    elif input_file.endswith('.csv'): #this part works
        gals = []
        with open(input_file) as inp:
            for row in inp:
                gals.append(row.split()[0])
    elif input_file.endswith('txt'):
        gals = []
        with open(input_file) as inp:
            gals = inp.read().splitlines()
    return gals

def get_coords(gals):
    """
        Takes list of galaxies and looks up their coordinates by name.
        If no name found: warn, skip, remove galaxy from list

        Returns:
            gals: list of galaxies minus those that weren't found
            start_coord: list of coordinates corresponding to center of galaxies in 'gals'
    """
    start_coord = []
    bar = FillingCirclesBar('Loading galaxies', max = len(gals))
    for i in gals[:]: #gets all valid galaxies
        try:
            tempCoord = SkyCoord.from_name(i, frame = 'icrs')
            start_coord.append(tempCoord)
            bar.next()
        except NameResolveError:
            print('\nSkipping',i,'because it couldn\'t be found.')
            gals.remove(i)
    bar.finish()
    return(gals,start_coord)

def coord_breakup(coord):
    """
        Breaks up a coordinate into its components
    """
    ra = Angle(coord.ra.hour,unit = u.hour)
    dec = coord.dec
    return(ra,dec)


def timeFix(s,m,h):
    """
        Fixes time to ensure it stays within normal range (0-60)
    """
    if(s>=60 or m>=60):
        while(s>=60 or m>=60):
            if s >= 60:
                m+=1
                s-=60
            if m >= 60:
                h+=1
                m-=60
    elif(s<0 or m<0):
        while(s<0 or m<0):
            if s < 0:
                m-=1
                s+=60
            if m < 0:
                h-=1
                m+=60
    return s,m,h

#------------------------AV Utility Functions Below------------------------#

def fourCoord(distance,ra,dec):
    """
        Gets four coordinates a specified distance away from the center of the galaxy
        Inputs:
            distance: distance in arcminutes
            ra: radial component of the coordinate
            dec: declination component of the coordinate
        Outputs:
            cardinals: list of four coordinates *distance* arcminutes away from the center of the specified galaxy. (North, East, South, West)
    """
    ds = distance*4
    cardinals = [None]*4 #n = 0, e = 1, s = 2, w = 3
    #e
    ds/=math.cos(math.radians(dec.degree))
    h = ra.hms.h
    m = ra.hms.m
    s = ra.hms.s+ds
    (s,m,h) = timeFix(s,m,h) #keep time within allowed range
    rad = Angle((h,m,s), unit = u.hour)
    rad = Angle(rad.to_string(unit=u.hour),u.hour)
    cardinals[1] = rad.to_string()+" "+dec.to_string()

    #n
    decli = dec.arcminute+distance
    decl = Angle(decli,u.arcminute)
    decl = Angle(decl.to_string(unit=u.degree),u.degree)
    cardinals[0] = ra.to_string()+" "+decl.to_string()

    #w
    ds=ds*(-1)
    ds/=math.cos(math.radians(dec.degree))
    h = ra.hms.h
    m = ra.hms.m
    s = ra.hms.s+ds
    (s,m,h) = timeFix(s,m,h) #keep time within allowed range
    rad = Angle((h,m,s), unit = u.hour)
    rad = Angle(rad.to_string(unit=u.hour),u.hour)
    cardinals[3] = rad.to_string()+" "+dec.to_string()

    #s
    decli = dec.arcminute-distance
    decl = Angle(decli,u.arcminute)
    decl = Angle(decl.to_string(unit=u.degree),u.degree)
    cardinals[2] = ra.to_string()+" "+decl.to_string()

    #print(cardinals)
    return cardinals; #performs transformation of initial coordinate into cardinal coordinates


def scaleChecker(a_v):
    avg = np.average(a_v)
    if avg >1.12*a_v[0][0]:
        return True
    else:
        return False


def checkCoords(ra,dec,gal_name):
    curVal = [None]*4 #n = 0, e = 1, s = 2, w = 3
    #get values for each arcminute
    # print('\nChecking Av values for',gal_name)

    cardinals = fourCoord(20,ra,dec)
    for i in range(0,4):
        C = coordinates.SkyCoord(cardinals[i], frame = 'fk5')
        table = IrsaDust.get_extinction_table(C,show_progress = False)
        curVal[i] = (table['A_SandF'][2])
    avgTwenty = np.average(curVal)

    cardinals = fourCoord(0,ra,dec)
    C = coordinates.SkyCoord(cardinals[0],frame = 'fk5')
    table = IrsaDust.get_extinction_table(C,show_progress = False)
    centerVal = (table['A_SandF'][2])
    if centerVal > 1.12*(avgTwenty):
        return True
    else:
        return False

def tableFill(distance, ra, dec, gal_name,file_obj):
    """
        Saves a table to Excel with Av values up to [distance] away from the center [ra, dec] in the four cardinal directions.
        Inputs:
            distance: distance from center in arcminutes
            ra: radial component of central coordinate
            dec: declination component of central coordinate
            gal_name: name of current galaxy
        Outputs:
            a_v: list of lists of Av values at each arcminute away from center
                -size(a_v) = [[Av * 4]*distance]

        IN THE PROCESS OF CLEANING THIS UP
        Things I think I don't need:
            Table
            DEAL WITH THIS LATER: 11/1/18
            DEALING WITH THIS NOW: 11/20/18
    """
    a_v = [None]*(distance+1)
    curVal = [None]*4 #n = 0, e = 1, s = 2, w = 3
    #get values for each arcminute
    print('\nGetting Av values for',gal_name)
    bar = ChargingBar('Fetching', max = distance+1)
    for arc_minute in range(0,distance+1):
        cardinals = fourCoord(arc_minute, ra, dec)
        for i in range(0,4):
            C = coordinates.SkyCoord(cardinals[i], frame = 'fk5')
            table = IrsaDust.get_extinction_table(C,show_progress = False)
            curVal[i] = (table['A_SandF'][2])
        a_v[arc_minute] = tuple(curVal)
        bar.next()
    bar.finish()
    print('Generating table')

    n = [gal_name]
    namesTable = Table([n], names=('n'))
    final_name = namesTable.to_pandas()

    av_table = Table(None)
    Am = Column(name = 'Arcminute')
    North = Column(name = 'North')
    East = Column(name = 'East')
    South = Column(name = 'South')
    West = Column(name = 'West')
    av_table.add_columns([Am,North, East, South, West])
    # print(a_v)
    for arcminute in range(0,len(a_v)):
        av_table.add_row()
        av_table[arcminute][0] = arcminute
        for i in range(0,4):
            av_table[arcminute][i+1] = a_v[arcminute][i]
    av_table.add_row()
    # print(av_table)

    for i in range(0,5): #this adds a blank line to the table to separate queries
        av_table[arcminute+1][i] = None

    final_vals = av_table.to_pandas()
    from pandas import ExcelWriter
    final_name.to_csv(file_obj, header =False, index = False)
    final_vals.to_csv(file_obj, header =True, index = False, sep = ',')

    return(a_v) #returns LIST of a_v values




def picSaver(directory, ra, dec, galaxy_name):
    """
        Gets image from IRSA for a given coordinate and saves to chosen directory
        Inputs:
            directory: directory to save files in
            ra: radial component of center coordinate
            dec: declination component of center coordinate
            galaxy_name: name of current galaxy
        Outputs:
            None
    """
    imagelist = IrsaDust.get_image_list(SkyCoord(ra,dec).fk5, image_type="100um", radius=2*u.degree)
    image_file = download_file(imagelist[0],cache=True)
    image_data = fits.getdata(image_file, ext=0) #gets image from IRSA database
    plt.clf()
    plt.figure(1)
    plt.title(str(galaxy_name))
    plt.imshow(image_data,cmap='gray')
    plt.colorbar()
    plt.savefig(os.path.join(directory,'Pictures',(str(galaxy_name)+".png")))
    plt.clf()

def graphMaker(directory, a_v, galaxy_name):
    """
        Plots Av data from [tableFill] function and saves to chosen directory
        Inputs:
            directory: directory to save files in
            a_v: output array from [tableFill]
            galaxy_name: name of current galaxy
        Outputs:
            None
    """
    x = np.arange(len(a_v))
    a_v = np.array(a_v)
    plt.clf()
    plt.figure(1)
    plt.plot(x,a_v[:,0], color = "blue", marker = ".", label = "North")
    plt.plot(x,a_v[:,1], color = "red", marker = ".", label = "East")
    plt.plot(x,a_v[:,2], color = "green", marker = ".", label = "South")
    plt.plot(x,a_v[:,3], color = "black", marker = ".", label = "West")
    #plt.axvline(x=majAxis[j])
    plt.xlabel("Arcminutes from Center of Galaxy")
    plt.ylabel("A_v Value")
    plt.legend(loc='center right', shadow=True)
    plt.suptitle("A_v Values by Arcminute")
    plt.title(str(galaxy_name))
    plt.savefig(os.path.join(directory,'Graphs',(str(galaxy_name)+"e.png")))
    plt.clf()
