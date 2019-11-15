import numpy as np
import math

def NACA_4D( name, chord=1, n_points=100 ,separation=False ):
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
    Generacion de puntos "x" con una distribucion 1-cos(tita)
    yt funcion distribucion de espesor
    yc funcion de la linea de curvatura media, dyc su derivada
    tita pendiente en radianes de la linea de curvatura media
    '''
    tita = np.linspace(math.pi/2, 0, n_points, True)
    xc = [1-math.cos(tita[x]) for x in range(len(tita))]
    yt = [(5*XX)*((a0*math.sqrt(xc[x]))+a1*(xc[x])+a2*(math.pow(xc[x],2))+a3*(math.pow(xc[x],3))+a4*(math.pow(xc[x],4))) for x in range(len(tita))]
    yc = [(M/(math.pow(1-P,2)))*(1-2*P+2*P*xc[x]-(math.pow(xc[x],2))) for x in range(len(xc)) if xc[x]>=P] + [(M/(math.pow(P,2)))*(2*P*xc[x]-(math.pow(xc[x],2))) for x in range(len(xc)) if xc[x]<P]
    dyc = [(2*M/(math.pow(1-P,2)))*(P-xc[x]) for x in range(len(xc)) if xc[x]>=P] + [((2*M)/math.pow(P,2))*(P-xc[x]) for x in range(len(xc)) if xc[x]<P]
    t = [(math.atan(dyc[x])) for x in range(len(dyc))]
    
    # X,Y coordenas del extrados(u) e intrados(l) del Perfil, se redondea a 4 cifras despues de la coma
    Xu = [round((xc[x]-yt[x]*math.sin(t[x]))*chord,4) for x in range(len(xc))]
    Xl = [round((xc[x]+yt[x]*math.sin(t[x]))*chord,4) for x in range(len(xc))]
    Yu = [round(yc[x]+yt[x]*math.cos(t[x])*chord,4) for x in range(len(xc))]
    Yl = [round((yc[x]-yt[x]*math.cos(t[x]))*chord,4) for x in range(len(xc))]
    
    # Union de las curvas extrados e intrados, salida coords con listado de puntos. Se elimina puntos repetidos en extremos de vectores
    Xl.pop()
    Yl.pop()
    X = Xu + Xl[::-1]
    Y = Yu + Yl[::-1]
    coords = [( X[x],Y[x] ) for x in range( len(X) )]
    
    # Filtrado de valores repetidos de X cerca del borde de ataque. Se invierte loop del pop() para que no haya cambios de indexación
    index=[]
    for i in range(len(coords)-1):
        if abs(coords[i][0]-coords[i+1][0])<0.00009:
            index.append(i)
    try:
        for i in range(len(index)-1,-1,-1):
            coords.pop(index[i])
    except:
        None
        
    return coords
