import matplotlib.pyplot as plt #se puede borrar usado para verificar
import numpy as np
import math
from NACA_4D import NACA_4D
from offset_airfoil import offset_airfoil
from scipy.interpolate import interp1d


def read_aorfoil(filename):
    ignore_head = 0
    coords = []
    with open(filename, "r") as fid:
        for line in fid.readlines()[ignore_head:]:
            data = line.split()
            coords.append((float(data[0]), float(data[1])))

    # Se asegura de que el punto inicial este repetido al final de la secuencia
#    if coords[0] != coords[-1]:
#        coords.append(coords[0])
    return coords

coords=read_aorfoil('NREL-S812.dat')

#X0=np.linspace(4, -4, 20, True)
#X1=[X0[i] for i in range(len(X0))]
#X3=X1+X1[::-1]
#X3.pop(20)
#coords = [( X3[i],math.pow(X3[i],2) ) for i in range( 0,19)]+ [( X3[i],-math.pow(X3[i],2) ) for i in range( 19,39 )]

#X0=np.linspace(4, -4, 20, True)
#coords = [( X0[i],math.pow(X0[i],2) ) for i in range( 0,20)]
#coords=coords[::-1]


#coords=NACA_4D('2412',1,200)

coordsoffset=offset_airfoil(coords,0.001)

X=[coords[i][0] for i in range(len(coords))]
Y=[coords[i][1] for i in range(len(coords))]
borrar1=[coordsoffset[i][0] for i in range(len(coordsoffset))]
borrar2=[coordsoffset[i][1] for i in range(len(coordsoffset))]

plt.axis('equal')
plt.plot(borrar1,borrar2,'*')
plt.plot(X,Y,'*')
plt.show()