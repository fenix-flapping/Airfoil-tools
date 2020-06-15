'''
Funcion que busca valores especificos de la ordenada del extrados e intrados y devuelve el indice.
Las divisiones fueron definidas en dos partes antes del 25% de la cuerda y tres partes despues. Modificando la variable "division"
es posible modificar estas divisiones, se realiza en sentido antihorario desde el borde de fuga.
No posee proteccion ante pedido de valores erroneos o fuera de escala

'''
def found_division_index(coords,division):
    point_division_extr = []
    point_division_intr = []

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

    return point_division



