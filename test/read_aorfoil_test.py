from scipy.interpolate import interp1d
import numpy as np
import math
import matplotlib.pyplot as plt #se puede borrar usado para verificar

filename='NREL-S812.dat'
distribution='Double'
n_points=100
chord=1
precision=6


ignore_head=0 # Elimina el titulo del archivo .dat
coords = []
with open(filename, "r") as fid:
    for line in fid.readlines()[ignore_head:]:
        data = line.split()
        coords.append((float(data[0]), float(data[1])))

# redondeo de numeros de puntos y corrección al numero de puntos
n_points=round(n_points/2)+1

# Dividir perfil en extrados e intrados para armado de Splines
minimum = coords.index(min(coords))
Xu = [coords[i][0] for i in range(minimum+1)]
Xl = [coords[i][0] for i in range(minimum,len(coords))]
Yu = [coords[i][1] for i in range(minimum+1)]
Yl = [coords[i][1] for i in range(minimum,len(coords))]

# Armado de funciones Splines con control de lista vacia
if len(Xu)!=0:
    extr = interp1d( Xu, Yu, kind='linear')
if len(Xl)!=0:
    intr = interp1d( Xl, Yl, kind='linear')

#Generacion de puntos "x" con una distribucion 'Linear' x , 'Cosine' 1-cos(tita) , 'Double' 1-sin^2(tita)
if distribution=='Cosine':
    tita = np.linspace(math.pi/2, 0, n_points, True)
    xc = [1-math.cos(tita[x]) for x in range(len(tita))]
elif distribution=='Linear':
    xc = xc = np.linspace(1, 0, n_points, True)
elif distribution=='Double':
    tita = np.linspace(math.pi/2, 0, n_points, True)
    xc = [1-math.pow(math.cos(tita[x]),2) for x in range(len(tita))]
else:
    return print("Wrong distribution configuration of the Airfoil")
    sys.exit() # Frena el codigo ya que no es posible realizarse mas nada

# X,Y coordenas del extrados(u) e intrados(l) del Perfil, se redondea a "prec" cifras significativas
coords_extr = [(round(xc[x]*chord,precision) , round(extr(xc[x])*chord,precision)) for x in range(len(xc))]
coords_intr = [(round(xc[x]*chord,precision) , round(intr(xc[x])*chord,precision)) for x in range(len(xc))]

# Union de las curvas extrados e intrados, salida coords_final con listado de puntos. Se elimina punto repetido en extremos del vectore del extrados
coords_extr.pop()
coords_final = coords_extr + coords_intr[::-1]


X=[coords_final[i][0] for i in range(len(coords_final))]
Y=[coords_final[i][1] for i in range(len(coords_final))]

plt.axis('equal')
plt.plot(X,Y,'*')
plt.show()