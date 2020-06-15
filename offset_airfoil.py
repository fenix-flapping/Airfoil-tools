import math
import numpy as np
from scipy.interpolate import interp1d

def offset_airfoil(coords , offset_value, sharp):
    # Separo en coordenadas X e Y y defino el parametro "t" desde donde parametrizo la geometria
    X = [coords[i][0] for i in range(len(coords))]
    Y = [coords[i][1] for i in range(len(coords))]
    t = np.linspace(0, 1, len(coords))

    # Armado de funciones de parametrizacion con proteccion de lista vacia
    if len(X) != 0:
        x_interp = interp1d(t, X, kind='linear', fill_value='extrapolate')
        y_interp = interp1d(t, Y, kind='linear', fill_value='extrapolate')

    '''
    Calculo de la curva offset:
    Se analiza la derivada y'(t) y x'(t) y luego se aplica la ecuacion parametrica para una definir
    una curva paralela. Fuente:
    https://en.wikipedia.org/wiki/Parallel_curve#Parallel_curve_of_a_parametrically_given_curve
    '''

    Xoffset = []
    Yoffset = []
    dif = 0.001  # El valor debe ser menor a la cantidad de cifras significativas que se manejen en coords, sino genera error del spline (out of range)
    for i in range(len(coords)):
        dxt = (x_interp(t[i] + dif) - x_interp(t[i] - dif)) / (2 * dif)
        dyt = (y_interp(t[i] + dif) - y_interp(t[i] - dif)) / (2 * dif)

        Xoffset.append(X[i] + offset_value * (dyt / math.sqrt(dxt ** 2 + dyt ** 2)))
        Yoffset.append(Y[i] - offset_value * (dxt / math.sqrt(dxt ** 2 + dyt ** 2)))

    # Armado de listado de puntos offset con 6 cifras significativas
    coordsoffset = [(round(Xoffset[x], 6), round(Yoffset[x], 6)) for x in range(len(Xoffset))]

    # Agregado de punta de borde de fuga en perfiles con borde de ataque filosos
    if sharp == True:
        sharp_edge = X.index(min(X))
        coordsoffset.insert(sharp_edge + 1, (X[sharp_edge] - offset_value, 0))

    # Filtrado de valores cruzados de curvas offset (entrecruzamiento de vectores normales)
    '''
    Se divide el analisis en extrados e intrados (minimum)
    Se analizan cambios de signos en el eje de abscisas (X) de "coordsoffset"
    Se eliminan los puntos que generan cambios de signos en un loop (loop) 
    '''
    loop = 1
    while loop > 0:
        loop = 0
        index = []
        minimum = coordsoffset.index(min(coordsoffset))
        for i in range(len(coordsoffset) - 1):
            if i < minimum:
                if coordsoffset[i][0] - coordsoffset[i + 1][0] < 0:
                    index.append(i)
                    loop = 1
            else:
                if coordsoffset[i][0] - coordsoffset[i + 1][0] > 0:
                    index.append(i)
                    loop = 1
        # Eliminación de puntos
        if loop == 1:
            for i in range(len(index) - 1, -1, -1):
                coordsoffset.pop(index[i])

    return coordsoffset
