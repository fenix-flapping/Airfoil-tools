import math
from scipy.interpolate import interp1d

def offset_airfoil( coords , offset_value ):

    # Dividir perfil en extrados e intrados
    minimum = coords.index(min(coords))
    Xu = [coords[i][0] for i in range(minimum+1)]
    Xl = [coords[i][0] for i in range(minimum+1,len(coords))]
    Yu = [coords[i][1] for i in range(minimum+1)]
    Yl = [coords[i][1] for i in range(minimum+1,len(coords))]

    # Armado de funciones Splines con control de lista vacia
    if len(Xu)!=0:
        extr = interp1d( Xu, Yu, kind='linear')
    if len(Xl)!=0:
        intr = interp1d( Xl, Yl, kind='linear')

    X = [coords[i][0] for i in range(len(coords))]
    Y = [coords[i][1] for i in range(len(coords))]

    '''
    Calculo de la curva offset:
    Se analiza el angulo de la derivada alrededor de cada punto utilizando un diferencial "dif"
    Determinado el angulo se calcula el punto normal con una distancia "offset_value"
    '''
    Xoffset = []
    Yoffset = []
    dif = 0.0001 # El valor debe ser menor a la cantidad de cifras significativas que se manejen en coords, sino genera error del spline (out of range)
    for i in range( len(X) ):
        if i<minimum+1:
            try:
                ang = math.atan2( -extr(X[i]+dif) + extr(X[i]-dif) , -dif*2 ) # diferencias centrales
            except:
                try:
                    ang = math.atan2( -extr(X[i]+dif) + extr(X[i]) , -dif ) # diferencial hacia adelante
                except:
                    ang = math.atan2( -extr(X[i]) + extr(X[i]-dif) , -dif ) # diferencial hacia atras
        else:
            try:
                ang = math.atan2( intr(X[i]+dif) - intr(X[i]-dif) , dif*2 ) # diferencias centrales
            except:
                try:
                    ang = math.atan2( intr(X[i]+dif) - intr(X[i]) , dif ) # diferencial hacia adelante
                except:
                    ang = math.atan2( intr(X[i]) - intr(X[i]-dif) , dif ) # diferencial hacia atras
        Xoffset.append( X[i] + offset_value * math.sin(ang) )
        Yoffset.append( Y[i] - offset_value * math.cos(ang) )
        
    # Armado de listado de puntos offset con 6 cifras significativas
    coordsoffset = [ (round(Xoffset[x],6) , round(Yoffset[x],6)) for x in range( len(Xoffset) )]

    # Filtrado de valores cruzados de curvas offset (entrecruzamiento de vectores normales)
    '''
    Se divide el analisis en extrados e intrados (minimum)
    Se analizan cambios de signos en el eje de abscisas (X) de "coordsoffset"
    Se eliminan los puntos que generan cambios de signos en un loop (loop) 
    '''
    loop=1
    while loop>0:
        loop = 0
        index = []
        minimum = coordsoffset.index( min(coordsoffset) )
        for i in range( len(coordsoffset)-1 ):
            if i<minimum:
                if coordsoffset[i][0] - coordsoffset[i+1][0]<0:
                    index.append(i)
                    loop = 1
            else:
                if coordsoffset[i][0] - coordsoffset[i+1][0]>0:
                    index.append(i)
                    loop = 1
        # Eliminación de puntos
        if loop == 1:
            for i in range( len(index)-1 ,-1 ,-1 ):
                coordsoffset.pop( index[i] )

    return coordsoffset
