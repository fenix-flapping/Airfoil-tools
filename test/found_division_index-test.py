import math
from scipy.interpolate import interp1d
from NACA_4D import NACA_4D
from offset_airfoil import offset_airfoil
import os
import numpy as np
from read_airfoil import read_airfoil

#filename='NREL-S812.dat'
#coords=read_airfoil('NREL-S812.dat', distribution='Cosine')
coords = NACA_4D('4415', n_points=100, chord=1, separation=True)

#coords = offset_airfoil(coords1, 0.3)

# Valores de X donde se realizara la division
separation_point = coords.index(min(coords))
chord = coords[0][0] - coords[separation_point][0] # Determinar el valor de la cuerda
division=[chord*0.625 , chord*0.25 , chord*0.167 , chord*0.083]
    
'''
Funcion que busca valores especificos de la ordenada del extrados e intrados y devuelve el indice.
Las divisiones fueron definidas en dos partes antes del 25% de la cuerda y tres partes despues. Modificando la variable "division"
es posible modificar estas divisiones, se realiza en sentido antihorario desde el borde de fuga.
No posee proteccion ante pedido de valores erroneos o fuera de escala

'''

point_division_extr=[]
point_division_intr=[]

# Punto de division extrados intrados
separation_point = coords.index(min(coords))

# Calculo de los puntos de division
point_division_extr= [0] # El primer punto es siempre el "0"
    
# Analisis Extrados
j=0
for i in range(0,separation_point):
    if j<=3:
        if coords[i][0] < division[j]: 
            point_division_extr.append(i)
            j=j+1
    else:
        break

# Agregado de punto de divison del borde de ataque
point_division_extr.append(separation_point)

# Agregado de punto de divison del ultimo punto
point_division_intr.append(len(coords)-1)

# Analisis Intrados
j=0
for i in range( len(coords)-1 , separation_point, -1 ):
    if j<=3:
        if coords[i][0] < division[j]: 
            point_division_intr.append(i)
            j=j+1
    else:
        break

# El primer punto del intrados es el valor minimo del vector de coordenadas del perfil
point_division = point_division_extr[:] + point_division_intr[::-1]

