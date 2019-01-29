from utilities import *

def setup():
    gals = read_gals('../Inputs/testGals.csv')
    gals, start_coord = get_coords(gals)
    return gals, start_coord

if __name__ == '__main__':
    [gals, start_coord] = setup() #run setup to grab gals and coordinates
    for i in range(0,len(gals)):
        ra, dec = coord_breakup(start_coord[i])
        a_v = tableFill(2,ra,dec,gals[i])
        print(a_v)
        graphMaker('..',a_v,gals[i])

