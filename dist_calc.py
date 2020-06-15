import math

def dist_calc(coords,start_index, end_index):
    dist_acum=0

    for i in range(start_index,end_index):
        dist = math.sqrt((coords[i+1][0]-coords[i][0])**2+(coords[i+1][1]-coords[i][1])**2)
        dist_acum = dist_acum + dist

    return dist_acum