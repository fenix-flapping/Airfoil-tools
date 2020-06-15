import math
from NACA_4D import NACA_4D

coords = NACA_4D('4415', n_points=500, chord=1, separation=True)
#def dist_calc(coords,start_index, end_index):
start_index = 0
end_index = 10
dist_acum=0

for i in range(start_index,end_index):
    dist = math.sqrt((coords[i+1][0]-coords[i][0])**2+(coords[i+1][1]-coords[i][1])**2)
    dist_acum = dist_acum + dist
