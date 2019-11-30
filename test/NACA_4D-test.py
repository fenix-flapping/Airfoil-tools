import matplotlib.pyplot as plt #se puede borrar usado para verificar
import numpy as np
import math
from scipy.interpolate import interp1d
import sys

name='2412'
chord=1
n_points=100
separation = False
precision=5
distribution='Doble'

n_points=round(n_points/2) # redondeo de numeros de puntos y corrección al numero de puntos
coef=[]
# NACA MPXX, classification of the 4 digits
if len(name) == 4:
    for x in name:
        coef.append(x)
    M = int(coef[0])/100
    P = int(coef[1])/10
    XX = int(coef[2]+coef[3])/100
else:
    print("The NACA number must be four digits")
    

# Coeficientes de la función distribucion de espesor, el valor a4 define si el TE es abierto o cerrado
a0 = 0.2969 ; a1 = -0.1260 ; a2 = -0.3516 ; a3 = 0.2843;
if separation == False:
    a4 = -0.1036
else:
    a4 = -0.1015

'''
Generacion de puntos "x" con una distribucion 'Linear' x , 'Cosine' 1-cos(tita) , 'Double' 1-sin^2(tita)
yt funcion distribucion de espesor
yc funcion de la linea de curvatura media, dyc su derivada
tita pendiente en radianes de la linea de curvatura media
'''
if distribution=='Cosine':
    tita = np.linspace(math.pi/2, 0, n_points, True)
    xc = [1-math.cos(tita[x]) for x in range(len(tita))]
elif distribution=='Linear':
    xc = xc = np.linspace(1, 0, n_points, True)
elif distribution=='Double':
    tita = np.linspace(math.pi/2, 0, n_points, True)
    xc = [1-math.pow(math.cos(tita[x]),2) for x in range(len(tita))]
else:
    print("Wrong distribution configuration")
    sys.exit()

yt = [(5*XX)*((a0*math.sqrt(xc[x]))+a1*(xc[x])+a2*(math.pow(xc[x],2))+a3*(math.pow(xc[x],3))+a4*(math.pow(xc[x],4))) for x in range(len(xc))]
yc = [(M/(math.pow(1-P,2)))*(1-2*P+2*P*xc[x]-(math.pow(xc[x],2))) for x in range(len(xc)) if xc[x]>=P] + [(M/(math.pow(P,2)))*(2*P*xc[x]-(math.pow(xc[x],2))) for x in range(len(xc)) if xc[x]<P]
dyc = [(2*M/(math.pow(1-P,2)))*(P-xc[x]) for x in range(len(xc)) if xc[x]>=P] + [((2*M)/math.pow(P,2))*(P-xc[x]) for x in range(len(xc)) if xc[x]<P]
t = [(math.atan(dyc[x])) for x in range(len(dyc))]

# X,Y coordenas del extrados(u) e intrados(l) del Perfil, se redondea a "prec" cifras significativas
Xu = [round((xc[x]-yt[x]*math.sin(t[x]))*chord,precision) for x in range(len(xc))]
Xl = [round((xc[x]+yt[x]*math.sin(t[x]))*chord,precision) for x in range(len(xc))]
Yu = [round(yc[x]+yt[x]*math.cos(t[x])*chord,precision) for x in range(len(xc))]
Yl = [round((yc[x]-yt[x]*math.cos(t[x]))*chord,precision) for x in range(len(xc))]

# Union de las curvas extrados e intrados, salida coords con listado de puntos. Se elimina puntos repetidos en extremos de vectores
Xl.pop()
Yl.pop()
X = Xu + Xl[::-1]
Y = Yu + Yl[::-1]
coords = [( X[x],Y[x] ) for x in range( len(X) )]

# Filtrado de valores repetidos en el eje de abscisas(X) cerca del borde de ataque. Se invierte loop del pop() para que no haya cambios de indexación
index=[]
for i in range(len(coords)-1):
    if abs(coords[i][0]-coords[i+1][0]) < pow(10,-precision):
        index.append(i)
try:
    for i in range(len(index)-1,-1,-1):
        coords.pop(index[i])
except:
    None


X=[coords[i][0] for i in range(len(coords))]
Y=[coords[i][1] for i in range(len(coords))]
#borrar1=[coordsoffset[i][0] for i in range(len(coordsoffset))]
#borrar2=[coordsoffset[i][1] for i in range(len(coordsoffset))]

plt.axis('equal')
#plt.plot(borrar1,borrar2,'*')
plt.plot(X,Y,'*')
plt.show()