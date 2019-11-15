import matplotlib.pyplot as plt #se puede borrar usado para verificar
import numpy as np
import math
from NACA_4D import NACA_4D
from scipy.interpolate import interp1d
from scipy.interpolate import UnivariateSpline


coords=NACA_4D('8412',1,200)

hcapa=0.01

# Dividir perfil en extrados e intrados
min=coords.index(min(coords))
Xu=[coords[i][0] for i in range(min)]
Xl=[coords[i][0] for i in range(min,len(coords))]
Yu=[coords[i][1] for i in range(min)]
Yl=[coords[i][1] for i in range(min,len(coords))]

# Generación de funciones Spline
extr = interp1d( Xu, Yu, kind='linear')
intr = interp1d( Xl, Yl, kind='linear')
X=[coords[i][0] for i in range(len(coords))]
Y=[coords[i][1] for i in range(len(coords))]

aa=[]
Xoffset=[]
Yoffset=[]
# Calculo de la curva offset
for i in range(len(X)):
    dif=0.0001 # El valor debe ser menor a la cantidad de cifras que se manejen
    if i<min:
        try:
            ang=math.atan2(-extr(X[i]+dif)+extr(X[i]-dif),-dif*2) # diferencias centrales
        except:
            try:
                ang=math.atan2(-extr(X[i]+dif)+extr(X[i]),-dif) # diferencial hacia adelante
            except:
                ang=math.atan2(-extr(X[i])+extr(X[i]-dif),-dif) # diferencial hacia atras
    else:
        try:
            ang=math.atan2(intr(X[i]+dif)-intr(X[i]-dif),dif*2) # diferencias centrales
        except:
            try:
                ang=math.atan2(intr(X[i]+dif)-intr(X[i]),dif) # diferencial hacia adelante
            except:
                ang=math.atan2(intr(X[i])-intr(X[i]-dif),dif) # diferencial hacia atras
    Xoffset.append(X[i]+hcapa*math.sin(ang))
    Yoffset.append(Y[i]-hcapa*math.cos(ang))
    aa.append(ang)
    
plt.axis('equal')
plt.plot(Xoffset,Yoffset,'-')
plt.plot(X,Y,'*')
plt.show()
