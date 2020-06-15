from scipy.interpolate import interp1d
import numpy as np

def regenerate_points(coords, n_points=100, chord=1, precision=6):

    # Separo en coordenadas X e Y y defino el parametro "t" desde donde se parametrizo la geometria
    X = [coords[i][0] for i in range(len(coords))]
    Y = [coords[i][1] for i in range(len(coords))]
    t = np.linspace(0, 1, len(coords))

    # Armado de funciones de parametrizacion con proteccion de lista vacia
    if len(X) != 0:
        x_interp = interp1d(t, X, kind='linear', fill_value='extrapolate')
        y_interp = interp1d(t, Y, kind='linear', fill_value='extrapolate')

    # Generacion de puntos "t" con una distribucion 'Linear'
    tc = np.linspace(0, 1, n_points, True)

    # Se regeneran las coordenadas X e Y para el numero definido de puntos, se redondea a "precision" cifras significativas
    coords_final = [(round(float(x_interp(tc[i])), precision), round(float(y_interp(tc[i])), precision)) for i in range(len(tc))]

    return coords_final