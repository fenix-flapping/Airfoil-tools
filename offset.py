import matplotlib.pyplot as plt #se puede borrar usado para verificar
import numpy as np
import math
from NACA_4D import NACA_4D
from scipy.interpolate import interp1d
from scipy.interpolate import UnivariateSpline

a=NACA_4D('3318',1,50)

# Dividir perfil en extrados e intrados
xu=[]
xl=[]
yl=[]
yu=[]
for i in range(len(a)-1):
    x=a[i][0]
    y=a[i][1]
    if a[i][0]-a[i+1][0]>=0:
        xu.append(x)
        yu.append(y)
    else:
        xl.append(x)
        yl.append(y)
xl.append(a[len(a)-1][0])
yl.append(a[len(a)-1][1])
xu.append(xl[0])
yu.append(yl[0])




#plt.show()

f = interp1d( xu, yu, kind='quadratic')

hcapa=0.03
xoffset=[]
yoffset=[]
for i in range(len(xu)):
    xdif=xu[i]
    dif=0.0001
    if i==(len(xu)-1):
        ang=math.atan2(f(xdif+dif)-f(xdif),dif) # diferencial hacia adelante
        xoffset.append(xdif-hcapa*math.sin(ang))
        yoffset.append(f(xdif)+hcapa*math.cos(ang))
    elif i==0:
        ang=math.atan2(f(xdif)-f(xdif-dif),dif) # diferencial hacia atras
        xoffset.append(xdif-hcapa*math.sin(ang))
        yoffset.append(f(xdif)+hcapa*math.cos(ang))
    else:
        ang=math.atan2(f(xdif+dif)-f(xdif-dif),dif*2) # diferencias centrales
        xoffset.append(xdif-hcapa*math.sin(ang))
        yoffset.append(f(xdif)+hcapa*math.cos(ang))
        
#plt.figure(figsize=(10.24, 2.56))
plt.axis('square')
plt.plot(xl,yl,'.')
plt.plot(xu,yu,'*')
plt.plot(xoffset,yoffset,'-')
plt.show()

'''
a=NACA_4D('3312')
x=[a[x][0] for x in range( len(a) )]
y=[a[x][1] for x in range( len(a) )]

f = interp1d( x, y, kind='linear')
y1=[float(f(x[a])) for a in range( len(x) )]

plt.plot(x,y,'.')
plt.plot(x,y1)
plt.show()

# Primero dividir el perfil en parte superior e inferior ya que genera errores en el spline
dydx=[]
for i in range(len(x)):
    xdif=x[i]
    if i==0 or i==len(x) or xdif==0:
        dif=0
        dydx.append(math.atan2(f(xdif-dif)-f(xdif+dif),dif*2))
    else:
        dif=0.001
        dydx.append(math.atan2(f(xdif-dif)-f(xdif+dif),dif*2))
'''