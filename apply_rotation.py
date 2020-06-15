import numpy as np

def apply_rotation(coords, angle, center=[0.25, 0]):
    center = np.array(center)
    theta = np.radians(angle)  # convierte en radianes los gradosº
    c, s = np.cos(theta), np.sin(theta)  # asigna valores a mas de una variable con la coma
    R = np.array(((c, -s), (s, c))).T  # Transpuesta de la matriz
    coords_rotated = []
    for point in coords:
        vector = point - center
        vector_rotated = R.dot(vector)  # Producto vectorial de matriz de rotacion con vector de cada coordenada
        coords_rotated.append(tuple(vector_rotated + center))  # calculo rotacion del perfil
    return coords_rotated