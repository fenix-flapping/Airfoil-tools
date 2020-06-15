import numpy as np
import math
from scipy.interpolate import interp1d
from NACA_4D import NACA_4D
from offset_airfoil import offset_airfoil
from found_division_index import found_division_index
from apply_rotation import apply_rotation
from regenerate_points import regenerate_points
import os
from read_airfoil import read_airfoil
from dist_calc import dist_calc

class config:
    # GEOMETRIA DEL DOMINIO
    # Numero de puntos aplicados al perfil y superficies bordeantes.
    n_points = 200
    # Posee el perfil con borde de ataque filoso?. True/False - (si/no).
    sharp = False
    # Altura contorno perfil
    countour_airfoil_height = 0.3
    # Altura del dominio en cuerdas de perfil a partir del eje x.
    domain_height = 3
    # Longitud de la estela en numero de cuerdas de perfil a partir del BF.
    wake_long = 4
    # Altura Dominio interno en cuerdas de perfil a partir del eje x. Debe ser menor a "domain_height" y mayor al contorno exterior del perfil
    domain_int_height = 1.5

    #DEFINICION DEL MALLADO
    # Modifica globalmente el numero de celdas. Util para analisis de convergencia. No modifica valores en la capa limite.
    global_cell = 1
    # Numero de celdas sobre el perfil.
    airfoil_cell = 100
    # Numero de celdas en el contorno exterior.
    ol_cell = 20
    # Progresion del espesor de las celdas del contorno exterior. <1 mas celdas hacia el perfil ; >1 mas celdas hacia el infinito
    ol_prog_cell = 0.95
    # Densidad de celdas dominio exterior - Celdas por unidad
    domain_dens_celll = 2
    # Densidad de celdas dominio interior - Celdas por unidad
    domain_int_dens_cell = 5

    # CONFIGURACIÓN DE CAPA LIMITE. Sino se utiliza en el analisis ignorar esta parte.
    # Agregado de capa limite al analisis. True/False - (si/no).
    bl = False
    # Numero de celdas totales en la capa limite.
    bl_cell = 10
    # Altura de la primera celda de la capa limite. Se obtiene de determinar el y+ buscado.
    bl_first_cell = 0.002
    # Progresion de la longitud de la celdas de la capa limite. <1 decrece la altura ; >1 incrementa la altura
    bl_prog_cell = 1.2


# Valores de ingreso en la funcion, que NO son configuración.
# Angulo de ataque en grados.
ang = 45
coords = NACA_4D('4415', 1, config.n_points, separation= False)
#coords=read_airfoil('goe05k.dat')
#coords=read_airfoil('NREL-S812.dat')

'''
INICIO DE LA FUNCION
'''
#def geo_airfoil_low_angle(coords, angle, config)


# Calculo capa altura capa limite
height_bl = config.bl_first_cell * ((1 - math.pow(config.bl_prog_cell, config.bl_cell)) / (1 - config.bl_prog_cell))

# Regeneracion de puntos del Perfil
coords_airfoil = regenerate_points(coords, config.n_points, precision=6)

# Armado de puntos
start_point = 1  # Inicio de numeracion de puntos

# Analisis de separacion de puntos de borde de fuga, se debe tener un tratamiento de la malla diferente segun sea el caso.
if coords_airfoil[0] == coords_airfoil[len(coords_airfoil) - 1]:
    separation = False
else:
    separation = True

# Valores de X donde se realizara la division
separation_point = coords_airfoil.index(min(coords_airfoil)) # Separacion extrados-intrados
chord = coords_airfoil[0][0] - coords_airfoil[separation_point][0] # Determinar el valor de la cuerda
division = [chord*0.625 , chord*0.25 , chord*0.167 , chord*0.083] # Puntos de division, modificar con cuidado no agregar mas divisiones

with open(os.path.join("mesh", "perfil.geo"), "w") as file:
    # Escritura de Puntos del perfil
    count_point1 = start_point  # count1 es sumador de puntos del perfil
    coords_rotated = apply_rotation(coords_airfoil, ang) # Rotacion de puntos del perfil
    file.write('// Puntos del Perfil\n')
    for x, y in coords_rotated:
        file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point1, x, y))
        count_point1 = count_point1 + 1
    break_points_airfoil = found_division_index(coords_airfoil,division) # Busqueda de puntos de division del dominio

    # Escritura de Puntos de la capa limite
    if config.bl == True:
        count_point2 = 1000 + start_point # count_point2 es sumador de puntos de la capa limite, se alinea la numeracion de puntos
        # Calculo de puntos offset
        coords_offset_bl = offset_airfoil(coords, height_bl,config.sharp)
        coords_offset_bl = regenerate_points(coords_offset_bl, config.n_points, precision=6) # Regeneracion de puntos de la capa limite
        coords_rotated_bl = apply_rotation(coords_offset_bl, ang) # Rotacion de puntos de la capa limite
        file.write('\n// Boundary Layer Points\n')
        for x, y in coords_rotated_bl:
            file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point2, x, y))
            count_point2 = count_point2 + 1

    # Escritura de Puntos del contorno exterior
    count_point3 = 2000 + start_point # count_point3 es sumador de puntos de la capa limite, se alinea la numeracion de puntos
    coords_offset_ol = offset_airfoil(coords, config.countour_airfoil_height,config.sharp) # Calculo de puntos offset
    coords_offset_ol = regenerate_points(coords_offset_ol, config.n_points, precision=6)  # Regeneracion de puntos del contorno exterior
    coords_rotated_ol = apply_rotation(coords_offset_ol, ang)  # Rotacion de puntos del contorno exterior
    file.write('\n// Outer Layer Points\n')
    for x, y in coords_rotated_ol:
        file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point3, x, y))
        count_point3 = count_point3 + 1

    # Armado de lineas
    if config.bl == False:
        # Armado de lineas del perfil
        file.write('\n// Airfoil Lines\n')
        count_line1 = 1  # count_line1 es sumador de lineas del perfil
        for i in range(len(break_points_airfoil)-2):
            file.write("Line(%i) = {%i:%i};\n" % (count_line1, break_points_airfoil[i] + 1, break_points_airfoil[i + 1] + 1))
            count_line1 = count_line1 + 1
        # Procedimiento de cierre del perfil diferente segun exista o no separacion de puntos en el borde de fuga
        i = len(break_points_airfoil) - 2
        if separation == True:
            file.write("Line(%i) = {%i:%i};\n" % (count_line1, break_points_airfoil[i] + 1, break_points_airfoil[i + 1] + 1))
            count_line1 = count_line1 + 1
        else:
            file.write("Line(%i) = {%i:%i,%i};\n" % (count_line1, break_points_airfoil[i] + 1, break_points_airfoil[i + 1], break_points_airfoil[0] + 1))
            count_line1 = count_line1 + 1

        # Armado de lineas del contorno exterior
        file.write('\n// Outer Layer Lines\n')
        count_line3 = 201  # count_line3 es sumador de lineas del contorno exterior
        for i in range(len(break_points_airfoil)-1):
            file.write("Line(%i) = {%i:%i};\n" % (count_line3, break_points_airfoil[i] + 2001, break_points_airfoil[i + 1] + 2001))
            count_line3 = count_line3 + 1

        # Armado de lineas de division de corte
        file.write('\n// Division Lines\n')
        count_line4 = 1101  # count_line4 es sumador de lineas de corte de perfil - contorno exterior
        for i in range(len(break_points_airfoil)-1):
            file.write("Line(%i) = {%i, %i};\n" % (count_line4, break_points_airfoil[i] + 2001, break_points_airfoil[i] + 1))
            count_line4 = count_line4 + 1
        # El armado de la linea de division final es diferente segun exista separacion del borde de fuga o no
        i = len(break_points_airfoil) - 1
        if separation == True:
            file.write("Line(%i) = {%i, %i};\n" % (count_line4, break_points_airfoil[i] + 2001, break_points_airfoil[i] + 1))
            count_line4 = count_line4 + 1
        else:
            file.write("Line(%i) = {%i, %i};\n" % (count_line4, break_points_airfoil[i] + 2001, break_points_airfoil[0] + 1))
            count_line4 = count_line4 + 1

        # Armado de superficies
        count_sup1 = 1  # count_sup1 es sumador de superficies
        file.write("\n// Surfaces - Airfoil\n")

        # Armado de Superficies del contorno del perfil
        file.write("\n// Surfaces - Outer Layer\n")
        for i in range(len(break_points_airfoil) - 1):
            file.write("Line Loop(%i) = {%i, %i, %i, %i};\n" % (count_sup1, (i + 1), -(i + 1102) ,- (i + 201) , (i + 1101)))
            file.write("Plane Surface(%i) = {%i};\n" % (count_sup1, count_sup1))
            count_sup1 = count_sup1 + 1

        # Transfinite y Recombine de Superficies del contorno del perfil
        file.write("\n// Surfaces Transfinite and Recombine - Outer Layer\n")
        for i in range(1, len(break_points_airfoil)):
            file.write(" Recombine Surface {%i};\n" % (i))
            file.write(" Transfinite Surface {%i};\n" % (i))

    else:

        # Armado de lineas del perfil
        file.write('\n// Airfoil Lines\n')
        count_line1 = 1  # count_line1 es sumador de lineas del perfil
        for i in range(len(break_points_airfoil)-2):
            file.write("Line(%i) = {%i:%i};\n" % (count_line1, break_points_airfoil[i] + 1, break_points_airfoil[i + 1] + 1))
            count_line1 = count_line1 + 1
        # Procedimiento de cierre del perfil diferente segun exista o no separacion de puntos en el borde de fuga
        i = len(break_points_airfoil) - 2
        if separation == True:
            file.write("Line(%i) = {%i:%i};\n" % (count_line1, break_points_airfoil[i] + 1, break_points_airfoil[i + 1] + 1))
            count_line1 = count_line1 + 1
        else:
            file.write("Line(%i) = {%i:%i,%i};\n" % (count_line1, break_points_airfoil[i] + 1, break_points_airfoil[i + 1], break_points_airfoil[0] + 1))
            count_line1 = count_line1 + 1

        # Armado de lineas de la capa limite
        file.write('\n// Boundary Layer Lines\n')
        count_line2 = 101  # count_line2 es sumador de lineas de la capa limite
        for i in range(len(break_points_airfoil)-1):
            file.write("Line(%i) = {%i:%i};\n" % (count_line2, break_points_airfoil[i] + 1001, break_points_airfoil[i + 1] + 1001))
            count_line2 = count_line2 + 1

        # Armado de lineas del contorno exterior
        file.write('\n// Outer Layer Lines\n')
        count_line3 = 201  # count_line3 es sumador de lineas del contorno exterior
        for i in range(len(break_points_airfoil)-1):
            file.write("Line(%i) = {%i:%i};\n" % (count_line3, break_points_airfoil[i] + 2001, break_points_airfoil[i + 1] + 2001))
            count_line3 = count_line3 + 1

        # Armado de lineas de division de corte
        file.write('\n// Division Lines Airfoil\n')
        count_line4 = 1001  # count_line4 es sumador de lineas de corte de perfil - capa limite
        for i in range(len(break_points_airfoil)-1):
            file.write("Line(%i) = {%i, %i};\n" % (count_line4, break_points_airfoil[i] + 1001, break_points_airfoil[i] + 1))
            count_line4 = count_line4 + 1
        # El armado de la linea de division final es diferente segun exista separacion del borde de fuga o no
        i = len(break_points_airfoil) - 1
        if separation == True:
            file.write("Line(%i) = {%i, %i};\n" % (count_line4, break_points_airfoil[i] + 1001, break_points_airfoil[i] + 1))
            count_line4 = count_line4 + 1
        else:
            file.write("Line(%i) = {%i, %i};\n" % (count_line4, break_points_airfoil[i] + 1001, break_points_airfoil[0] + 1))
            count_line4 = count_line4 + 1
        count_line5 = 1101  # count_line5 es sumador de lineas de corte de capa limite - contorno exterior
        for i in range(len(break_points_airfoil)):
            file.write("Line(%i) = {%i, %i};\n" % (count_line5, break_points_airfoil[i] + 2001, break_points_airfoil[i] + 1001))
            count_line5 = count_line5 + 1

        # Armado de superficies
        count_sup1 = 1  # count_sup1 es sumador de superficies del contorno del perfil
        file.write("\n// Surfaces - Airfoil\n")

        # Armado de Superficies del contorno del perfil
        file.write("\n// Surfaces - Boundary Layer\n")
        for i in range(len(break_points_airfoil) - 1):
            file.write("Line Loop(%i) = {%i, %i, %i, %i};\n" % (count_sup1, (i + 1), -(i + 1002) ,- (i + 101) , (i + 1001)))
            file.write("Plane Surface(%i) = {%i};\n" % (count_sup1, count_sup1))
            count_sup1 = count_sup1 + 1

        # Transfinite y Recombine de Superficies del contorno del perfil
        file.write("\n// Surfaces Transfinite and Recombine - Boundary Layer\n")
        for i in range(1, len(break_points_airfoil)):
            file.write(" Recombine Surface {%i};\n" % (i))
            file.write(" Transfinite Surface {%i};\n" % (i))

        # Armado de Superficies del contorno del contorno exterior
        file.write("\n// Surfaces - Outer Layer\n")
        for i in range(len(break_points_airfoil) - 1):
            file.write("Line Loop(%i) = {%i, %i, %i, %i};\n" % (count_sup1, (i + 101), -(i + 1102) ,- (i + 201) , (i + 1101)))
            file.write("Plane Surface(%i) = {%i};\n" % (count_sup1, count_sup1))
            count_sup1 = count_sup1 + 1

        # Transfinite y Recombine de Superficies del contorno exterior
        file.write("\n// Surfaces Transfinite and Recombine - Outer Layer\n")
        for i in range(len(break_points_airfoil), count_sup1):
            file.write(" Recombine Surface {%i};\n" % (i))
            file.write(" Transfinite Surface {%i};\n" % (i))

    # Armado de Linea de union de borde de fuga abierto
    if separation == True:
        file.write("\n// Open Trailing Edge Line\n")
        file.write("Line(%i) = {%i, %i};\n" % (count_line1, break_points_airfoil[len(break_points_airfoil)-1] + 1, break_points_airfoil[0] + 1))
        count_line1 = count_line1 + 1

    # Armado de puntos del dominio
    file.write("\n// Domain Points\n")
    count_point4 = 4001 # count_point4 es sumador de puntos del dominio
    file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, chord*0.25, config.domain_height * chord))
    count_point4 = count_point4 + 1
    file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4,-config.domain_height * chord, 0))
    count_point4 = count_point4 + 1
    file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, chord*0.25, -config.domain_height * chord))
    count_point4 = count_point4 + 1
    file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, (chord * (1 + config.wake_long)), -config.domain_height * chord))
    count_point4 = count_point4 + 1
    file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, (chord * (1 + config.wake_long)), -config.domain_int_height * chord))
    count_point4 = count_point4 + 1
    file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, (chord * (1 + config.wake_long)), config.domain_int_height * chord))
    count_point4 = count_point4 + 1
    file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, (chord * (1 + config.wake_long)), config.domain_height * chord))
    count_point4 = count_point4 + 1

    # Armado de puntos del dominio interno
    file.write("\n// Internal Domain Points\n")
    count_point5 = 3001 # count_point5 es sumador de puntos del dominio interno
    file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point5, chord*0.25, config.domain_int_height * chord))
    count_point5 = count_point5 + 1
    file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point5,-config.domain_int_height * chord, 0))
    count_point5 = count_point5 + 1
    file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point5, chord*0.25, -config.domain_int_height * chord))
    count_point5 = count_point5 + 1

    # Armado de Lineas del dominio
    file.write("\n// Domain Lines\n")
    count_line7 = 1301  # count_line7 es sumador de lineas del borde exterior del dominio
    file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (10000, 0.25*chord, 0)) # Centro de la elipse
    file.write("Ellipse(%i) = {%i, %i, %i, %i};\n" % (count_line7, 4001, 10000, 4002, 4002))
    count_line7 = count_line7 + 1
    file.write("Ellipse(%i) = {%i, %i, %i, %i};\n" % (count_line7, 4002, 10000, 4002, 4003))
    count_line7 = count_line7 + 1
    file.write("Line(%i) = {%i, %i};\n" % (count_line7, 4003, 4004))
    count_line7 = count_line7 + 1
    file.write("Line(%i) = {%i, %i};\n" % (count_line7, 4004, 4005))
    count_line7 = count_line7 + 1
    file.write("Line(%i) = {%i, %i};\n" % (count_line7, 4005, 4006))
    count_line7 = count_line7 + 1
    file.write("Line(%i) = {%i, %i};\n" % (count_line7, 4006, 4007))
    count_line7 = count_line7 + 1
    file.write("Line(%i) = {%i, %i};\n" % (count_line7, 4007, 4001))
    count_line7 = count_line7 + 1

    # Armado de Lineas del dominio interno
    file.write("\n// Internal Domain Lines\n")
    count_line8 = 1401  # count_line7 es sumador de lineas del borde exterior del dominio
    file.write("Line(%i) = {%i, %i};\n" % (count_line8, 4006, 3001))
    count_line8 = count_line8 + 1
    file.write("Ellipse(%i) = {%i, %i, %i, %i};\n" % (count_line8, 3001, 10000, 3002, 3002))
    count_line8 = count_line8 + 1
    file.write("Ellipse(%i) = {%i, %i, %i, %i};\n" % (count_line8, 3002, 10000, 3002, 3003))
    count_line8 = count_line8 + 1
    file.write("Line(%i) = {%i, %i};\n" % (count_line8, 3003, 4005))
    count_line8 = count_line8 + 1

    # Armado de Superficies del dominio interno
    file.write('\n// Surface Internal Domain\n')
    if separation == True:
        if config.bl == True:
            file.write("Line Loop(%i) = {1111, 1011, 11, -1001, -1101, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210};\n" % (count_sup1))
            count_sup1 = count_sup1 + 1
            file.write("Curve Loop(%i) = {1401, 1402, 1403, 1404, 1305};\n" % (count_sup1))
            file.write("Plane Surface(%i) = {%i, %i};\n" % (count_sup1 - 1, count_sup1, count_sup1 - 1))
            count_sup1 = count_sup1 + 1
        else:
            file.write("Line Loop(%i) = {1111, 11, -1101, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210};\n" % (count_sup1))
            count_sup1 = count_sup1 + 1
            file.write("Curve Loop(%i) = {1401, 1402, 1403, 1404, 1305};\n" % (count_sup1))
            file.write("Plane Surface(%i) = {%i, %i};\n" % (count_sup1 - 1, count_sup1, count_sup1 - 1))
            count_sup1 = count_sup1 + 1
    else:
        if config.bl == True:
            file.write("Line Loop(%i) = {1111, 1011, -1001, -1101, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210};\n" % (count_sup1))
            count_sup1 = count_sup1 + 1
            file.write("Curve Loop(%i) = {1401, 1402, 1403, 1404, 1305};\n" % (count_sup1))
            file.write("Plane Surface(%i) = {%i, %i};\n" % (count_sup1 - 1, count_sup1, count_sup1 - 1))
            count_sup1 = count_sup1 + 1
        else:
            file.write("Line Loop(%i) = {1111, -1101, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210};\n" % (count_sup1, ))
            count_sup1 = count_sup1 + 1
            file.write("Curve Loop(%i) = {1401, 1402, 1403, 1404, 1305};\n" % (count_sup1))
            file.write("Plane Surface(%i) = {%i, %i};\n" % (count_sup1 - 1, count_sup1, count_sup1 - 1))
            count_sup1 = count_sup1 + 1
    count_sup1 = count_sup1 + 1

    # Armado de Superficies del dominio
    file.write('\n// Surface Domain\n')
    file.write("Curve Loop(%i) = {1306, 1307, 1301, 1302, 1303, 1304, -1404, -1403, -1402, -1401};\n" % (count_sup1))
    file.write("Plane Surface(%i) = {%i};\n" % (count_sup1 - 2, count_sup1))

    # Transfinite curvas airfoil - numero de celdas para el perfil
    long_airfoil = dist_calc(coords_airfoil, 0, len(coords_airfoil)-1) # Longitud del contorno del perfil
    transfin_airfoil = []
    w = 0.2 # Cambio de peso en la cantidad de elementos entre el borde de ataque y el resto del perfil
    weight = [(1-w),(1-w),(1-w),(1-w),(1+w*4),(1+w*4),(1-w),(1-w),(1-w),(1-w)]
    for i in range(len(break_points_airfoil)-1):
        long = dist_calc(coords_airfoil, break_points_airfoil[i], break_points_airfoil[i+1])
        transfin = round((long/long_airfoil) * config.airfoil_cell * config.global_cell * weight[i]) + 1
        if transfin < 2: # Minimo valor de celdas por seccion
            transfin = 2
        transfin_airfoil.append(transfin)
    file.write('\n// Transfinite Airfoil\n')
    if config.bl == True:
        for i in range(len(transfin_airfoil)):
            file.write("Transfinite Curve {%i, %i, %i} = %i Using Progression 1;\n" % (i + 1, i + 101, i + 201, transfin_airfoil[i]))
    else:
        for i in range(len(transfin_airfoil)):
            file.write("Transfinite Curve {%i,%i} = %i Using Progression 1;\n" % (i + 1, i + 201,transfin_airfoil[i]))

    # Transfinite capa limite
    if config.bl == True:
        file.write('\n// Transfinite Boundary Layer\n')
        file.write("Transfinite Curve {%i, %i, %i, %i, %i, %i, %i, %i, %i, %i, %i} = %i Using Progression %2.3f;\n" % (tuple(range(1001,1012)) + (config.bl_cell + 1, 1/config.bl_prog_cell)))

    # Transfinite contorno exterior
    file.write('\n// Transfinite Outer Layer\n')
    file.write("Transfinite Curve {%i, %i, %i, %i, %i, %i, %i, %i, %i, %i, %i} = %i Using Progression %2.3f;\n" % (tuple(range(1101,1112))+ ((config.ol_cell + 1) * config.global_cell, config.ol_prog_cell)))

    # Transfinite curvas Dominio
    file.write('\n// Transfinite Domain\n')
    file.write("Transfinite Curve {%i, %i} = %i Using Progression 1;\n" % (1307, 1303, chord * (0.75 + config.wake_long) * config.domain_dens_celll * config.global_cell))
    file.write("Transfinite Curve {%i, %i} = %i Using Progression 1;\n" % (1301, 1302, 0.5 * math.pi * config.domain_height * config.domain_dens_celll * config.global_cell))
    file.write("Transfinite Curve {%i, %i} = %i Using Progression 1;\n" % (1304, 1306, (config.domain_height - config.domain_int_height) * config.domain_dens_celll * config.global_cell))

    # Transfinite curvas Dominio interior
    file.write('\n// Transfinite Interior Domain\n')
    file.write("Transfinite Curve {%i, %i} = %i Using Progression 1;\n" % (1401, 1404, chord * (0.75 + config.wake_long) * config.domain_int_dens_cell * config.global_cell))
    file.write("Transfinite Curve {%i, %i} = %i Using Progression 1;\n" % (1402, 1403, 0.5 * math.pi * config.domain_int_height * config.domain_int_dens_cell * config.global_cell))
    file.write("Transfinite Curve {%i} = %i Using Progression 1;\n" % (1305, 2 * config.domain_int_height * config.domain_int_dens_cell * config.global_cell))


    # Definicion de las Physical Groups. No se pudo automatizar por tal caso se recomienda la version 4.5.6 del GMSH
    file.write('\n// Physical Groups\n')
    if config.bl == True:
        file.write("ids [] = Extrude {0, 0, -0.1} {Surface{1:22}; Layers {1} ; Recombine;};\n")
        file.write("""Physical Volume("Air") = {1:22};\n""")
        if separation == True:
            file.write("""Physical Surface("FrontandBack") = {21, 22, 20, 18, 17, 15, 12, 13, 16, 14, 11, 19, 9, 10, 1, 2, 3, 4, 8, 6, 7, 5, 1946, 1998, 1844, 1822, 1646, 1668, 1448, 1426, 1690, 1712, 1470, 1492, 1514, 1734, 1756, 1536, 1558, 1778, 1602, 1580, 1624, 1800};\n""")
            file.write("""Physical Surface("Inlet") = {1969, 1973};\n""")
            file.write("""Physical Surface("UpandDown") = {1965, 1977};\n""")
            file.write("""Physical Surface("Outlet") = {1885, 1961, 1981};\n""")
            file.write("""Physical Surface("Airfoil") = {1611, 1567, 1589, 1545, 1523, 1479, 1501, 1435, 1457, 1413, 1937};\n""")
        else:
            file.write("""Physical Surface("FrontandBack") = {21, 22, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 1, 3, 2, 4, 5, 6, 7, 8, 9, 10, 1993, 1941, 1646, 1668, 1712, 1690, 1734, 1756, 1778, 1800, 1822, 1844, 1426, 1624, 1448, 1602, 1470, 1580, 1492, 1514, 1536, 1558};\n""")
            file.write("""Physical Surface("Inlet") = {1968, 1964};\n""")
            file.write("""Physical Surface("UpandDown") = {1960, 1972};\n""")
            file.write("""Physical Surface("Outlet") = {1884, 1976, 1956};\n""")
            file.write("""Physical Surface("Airfoil") = {1611, 1589, 1567, 1545, 1523, 1501, 1479, 1457, 1435, 1413};\n""")
    else:
        file.write("ids [] = Extrude {0, 0, -0.1} {Surface{1:12}; Layers {1} ; Recombine;};\n")
        file.write("""Physical Volume("Air") = {1:12};\n""")
        if separation == True:
            file.write("""Physical Surface("FrontandBack") = {11, 12, 1, 10, 9, 8, 3, 2, 4, 5, 6, 7, 1716, 1768, 1426, 1448, 1470, 1492, 1514, 1536, 1558, 1580, 1602, 1624};\n""")
            file.write("""Physical Surface("Inlet") = {1739, 1743};\n""")
            file.write("""Physical Surface("UpandDown") = {1735, 1747};\n""")
            file.write("""Physical Surface("Outlet") = {1731, 1751, 1663};\n""")
            file.write("""Physical Surface("Airfoil") = {1435, 1413, 1457, 1479, 1501, 1523, 1545, 1567, 1589, 1611, 1711};\n""")
        else:
            file.write("""Physical Surface("FrontandBack") = {22, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1711, 1763, 1624, 1602, 1580, 1558, 1536, 1514, 1492, 1470, 1448, 1426};\n""")
            file.write("""Physical Surface("Inlet") = {1734, 1738};\n""")
            file.write("""Physical Surface("UpandDown") = {1730, 1742};\n""")
            file.write("""Physical Surface("Outlet") = {1662, 1746, 1726};\n""")
            file.write("""Physical Surface("Airfoil") = {1611, 1567, 1589, 1545, 1523, 1501, 1479, 1457, 1435, 1413};\n""")
