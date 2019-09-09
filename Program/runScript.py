from utilities import *
import argparse

def setup(listOfGals):
    gals = read_gals('../Inputs/'+str(listOfGals))
    gals, start_coord = get_coords(gals)
    return gals, start_coord

def openFile():
    f = open("av_vals.csv", 'w')
    return f

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process galaxies for AV data.')
    parser.add_argument('listOfGals', metavar='listOfGals', type=str, nargs='+', help='List of galaxies.')
    args = parser.parse_args()

    passed = []
    [gals, start_coord] = setup(args.listOfGals[0]) #run setup to grab gals and coordinates
    f = openFile()
    for i in range(0,len(gals)):
        ra, dec = coord_breakup(start_coord[i])
        verified = checkCoords(ra,dec,gals[i])
        if verified:
            passed.append(gals[i])
            a_v = tableFill(20,ra,dec,gals[i],f)
            graphMaker('..',a_v,gals[i])
            picSaver('..',ra,dec,gals[i])

    f.close()
    f = open('bright_gals.csv','w')
    for i in passed:
        f.write(i+'\n')
    f.close()

