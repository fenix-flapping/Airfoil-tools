import numpy as np
import math
import os
from offset_airfoil import offset_airfoil
from found_division_index import found_division_index
from apply_rotation import apply_rotation
from regenerate_points import regenerate_points
from dist_calc import dist_calc

def geo_airfoil_low_angle(coords, ang, config):
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

        # Armado de puntos del dominio - No estela
        file.write("\n// Domain Points\n")
        count_point4 = 3001 # count_point4 es sumador de puntos del dominio
        file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, coords_rotated_ol[0][0], config.domain_height * chord))
        count_point4 = count_point4 + 1
        file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, chord*0.25, config.domain_height * chord))
        count_point4 = count_point4 + 1
        file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4,-config.domain_height * chord, 0))
        count_point4 = count_point4 + 1
        file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, chord*0.25, -config.domain_height * chord))
        count_point4 = count_point4 + 1
        file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, coords_rotated_ol[len(coords_rotated_ol)-1][0], -config.domain_height * chord))
        count_point4 = count_point4 + 1

        # Armado de Lineas del dominio - No estela
        file.write("\n// Domain Lines\n")
        count_line7 = 1301  # count_line7 es sumador de lineas del borde exterior del dominio
        file.write("Line(%i) = {%i, %i};\n" % (count_line7, 3001, 3002))
        count_line7 = count_line7 + 1
        file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (10000, 0.25*chord, 0)) # Centro de la elipse
        file.write("Ellipse(%i) = {%i, %i, %i, %i};\n" % (count_line7, 3002, 10000, 3003, 3003))
        count_line7 = count_line7 + 1
        file.write("Ellipse(%i) = {%i, %i, %i, %i};\n" % (count_line7, 3003, 10000, 3003, 3004))
        count_line7 = count_line7 + 1
        file.write("Line(%i) = {%i, %i};\n" % (count_line7, 3004, 3005))
        count_line7 = count_line7 + 1

        # Armado de Lineas de division del dominio - No estela
        file.write("\n// Domain Division Lines\n")
        count_line6 = 1201  # count_line6 es sumador de lineas de corte de contorno exterior-dominio
        file.write("Line(%i) = {%i, %i};\n" % (count_line6, 3001, break_points_airfoil[0] + 2001))
        count_line6 = count_line6 + 1
        file.write("Line(%i) = {%i, %i};\n" % (count_line6, 3002, break_points_airfoil[2] + 2001))
        count_line6 = count_line6 + 1
        file.write("Line(%i) = {%i, %i};\n" % (count_line6, 3003, break_points_airfoil[5] + 2001))
        count_line6 = count_line6 + 1
        file.write("Line(%i) = {%i, %i};\n" % (count_line6, 3004, break_points_airfoil[8] + 2001))
        count_line6 = count_line6 + 1
        file.write("Line(%i) = {%i, %i};\n" % (count_line6, 3005, break_points_airfoil[10] + 2001))
        count_line6 = count_line6 + 1

        # Armado de Superficies, transfinite y recombine del contorno del contorno exterior. Se reutiliza count_sup1
        count_sup1 = count_sup1 + 1
        file.write("\n// Surfaces and Transfinite and Recombine - Domain\n")
        file.write("Line Loop(%i) = {%i, %i, %i, %i, %i};\n" % (count_sup1, 201, 202, -1202, -1301, 1201))
        file.write("Plane Surface(%i) = {%i};\n" % (count_sup1, count_sup1))
        file.write("Recombine Surface {%i};\n" % (count_sup1))
        file.write("Transfinite Surface {%i}={%i, %i, %i, %i};\n" % (count_sup1, break_points_airfoil[0] + 2001, break_points_airfoil[2] + 2001, 3002, 3001))
        count_sup1 = count_sup1 + 1
        file.write("Line Loop(%i) = {%i, %i, %i, %i, %i, %i};\n" % (count_sup1, 203, 204, 205, -1203, -1302, 1202))
        file.write("Plane Surface(%i) = {%i};\n" % (count_sup1, count_sup1))
        file.write("Recombine Surface {%i};\n" % (count_sup1))
        file.write("Transfinite Surface {%i}={%i, %i, %i, %i};\n" % (count_sup1, break_points_airfoil[2] + 2001, break_points_airfoil[5] + 2001, 3003, 3002))
        count_sup1 = count_sup1 + 1
        file.write("Line Loop(%i) = {%i, %i, %i, %i, %i, %i};\n" % (count_sup1, 206, 207, 208, -1204, -1303, 1203))
        file.write("Plane Surface(%i) = {%i};\n" % (count_sup1, count_sup1))
        file.write("Recombine Surface {%i};\n" % (count_sup1))
        file.write("Transfinite Surface {%i}={%i, %i, %i, %i};\n" % (count_sup1, break_points_airfoil[5] + 2001, break_points_airfoil[8] + 2001, 3004, 3003))
        count_sup1 = count_sup1 + 1
        file.write("Line Loop(%i) = {%i, %i, %i, %i, %i};\n" % (count_sup1, 209, 210, -1205, -1304, 1204))
        file.write("Plane Surface(%i) = {%i};\n" % (count_sup1, count_sup1))
        file.write("Recombine Surface {%i};\n" % (count_sup1))
        file.write("Transfinite Surface {%i}={%i, %i, %i, %i};\n" % (count_sup1, break_points_airfoil[8] + 2001, break_points_airfoil[10] + 2001, 3005, 3004))
        count_sup1 = count_sup1 + 1

        # Armado de puntos de la estela (se reutiliza el contador count_point4)
        file.write("\n// Wake Points;\n")
        file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, (chord * (1 + config.wake_long)), -config.domain_height * chord))
        count_point4 = count_point4 + 1
        file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, (chord * (1 + config.wake_long)), coords_rotated_ol[len(coords_offset_ol)-1][1] + config.wake_long * math.sin(np.radians(config.adj_wake))))
        count_point4 = count_point4 + 1
        file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, (chord * (1 + config.wake_long)), coords_rotated_ol[0][1] + config.wake_long * math.sin(np.radians(config.adj_wake))))
        count_point4 = count_point4 + 1
        file.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, (chord * (1 + config.wake_long)), config.domain_height * chord))
        count_point4 = count_point4 + 1

        # Armado de Lineas de la Estela
        file.write("\n// Wake Lines\n")
        file.write("Line(%i) = {%i, %i};\n" % (count_line7, 3006, 3005))
        count_line7 = count_line7 + 1
        file.write("Line(%i) = {%i, %i};\n" % (count_line7, 3006, 3007))
        count_line7 = count_line7 + 1
        file.write("Line(%i) = {%i, %i};\n" % (count_line7, 3007, 3008))
        count_line7 = count_line7 + 1
        file.write("Line(%i) = {%i, %i};\n" % (count_line7, 3009, 3008))
        count_line7 = count_line7 + 1
        file.write("Line(%i) = {%i, %i};\n" % (count_line7, 3009, 3001))
        count_line7 = count_line7 + 1

        # Armado de Lineas de division de la Estela (se reutiliza el contador count_line6)
        file.write("\n// Wake Division Lines\n")
        file.write("Line(%i) = {%i, %i};\n" % (count_line6, 3007, break_points_airfoil[len(break_points_airfoil)-1] + 2001))
        count_line6 = count_line6 + 1
        file.write("Line(%i) = {%i, %i};\n" % (count_line6, 3008, break_points_airfoil[0] + 2001))
        count_line6 = count_line6 + 1

        # Armado de Linea de union de borde de fuga abierto
        if separation == True:
            file.write("\n// Open Trailing Edge Line\n")
            file.write("Line(%i) = {%i, %i};\n" % (count_line1, break_points_airfoil[len(break_points_airfoil)-1] + 1, break_points_airfoil[0] + 1))

        # Armado de Superficies, transfinite y recombine de la estela (se reutiliza el contador count_sup1)
        file.write("\n// Surfaces and Transfinite and Recombine - Wake\n")
        file.write("Line Loop(%i) = {%i, %i, %i, %i};\n" % (count_sup1, 1305, 1205, -1206, -1306))
        file.write("Plane Surface(%i) = {%i};\n" % (count_sup1, count_sup1))
        file.write("Recombine Surface {%i};\n" % (count_sup1))
        file.write("Transfinite Surface {%i};\n" % (count_sup1))
        count_sup1 = count_sup1 + 1
        # Proceso diferente de armado para borde de fuga abierto y existencia de capa limite
        if separation == True:
            if config.bl == True:
                file.write("Line Loop(%i) = {%i, %i, %i, %i, %i, %i, %i, %i};\n" % (count_sup1, -1207, -1307, 1206, 1111, 1011, 11, -1001, -1101))
            else:
                file.write("Line Loop(%i) = {%i, %i, %i, %i, %i, %i};\n" % (count_sup1, -1207, -1307, 1206, 1111, 11, -1101))
        else:
            if config.bl == True:
                file.write("Line Loop(%i) = {%i, %i, %i, %i, %i, %i, %i};\n" % (count_sup1, -1207, -1307, 1206, 1111, 1011, -1001, -1101))
            else:
                file.write("Line Loop(%i) = {%i, %i, %i, %i, %i};\n" % (count_sup1, -1207, -1307, 1206, 1111, -1101))
        file.write("Plane Surface(%i) = {%i};\n" % (count_sup1, count_sup1))
        file.write("Recombine Surface {%i};\n" % (count_sup1))
        file.write("Transfinite Surface {%i} = {%i, %i, %i,%i};\n" % (count_sup1, 3008, 3007, break_points_airfoil[0] + 2001, break_points_airfoil[len(break_points_airfoil)-1] + 2001))
        count_sup1 = count_sup1 + 1
        file.write("Line Loop(%i) = {%i, %i, %i, %i};\n" % (count_sup1, 1207, -1201, -1309, 1308))
        file.write("Plane Surface(%i) = {%i};\n" % (count_sup1, count_sup1))
        file.write("Recombine Surface {%i};\n" % (count_sup1))
        file.write("Transfinite Surface {%i};\n" % (count_sup1))
        count_sup1 = count_sup1 + 1

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

        # Transfinite curvas dominio - No estela
        file.write("Transfinite Curve {%i} = %i Using Progression 1;\n" % (1301, transfin_airfoil[0] + transfin_airfoil[1] - 1))
        file.write("Transfinite Curve {%i} = %i Using Progression 1;\n" % (1302, transfin_airfoil[2] + transfin_airfoil[3] + transfin_airfoil[4] - 2))
        file.write("Transfinite Curve {%i} = %i Using Progression 1;\n" % (1303, transfin_airfoil[5] + transfin_airfoil[6] + transfin_airfoil[7] - 2))
        file.write("Transfinite Curve {%i} = %i Using Progression 1;\n" % (1304, transfin_airfoil[8] + transfin_airfoil[9] - 1))

        # Transfinite curvas Estela
        file.write('\n// Transfinite Wake\n')
        file.write("Transfinite Curve {%i, %i, %i, %i} = %i Using Progression %2.3f;\n" % (1309, 1207, 1206, 1305, (config.wake_div_cell + 1) * config.global_cell , config.wake_prog_cell))

        # Transfinite capa limite
        if config.bl == True:
            file.write('\n// Transfinite Boundary Layer\n')
            file.write("Transfinite Curve {%i, %i, %i, %i, %i, %i, %i, %i, %i, %i, %i} = %i Using Progression %2.3f;\n" % (tuple(range(1001,1012)) + (config.bl_cell + 1, 1/config.bl_prog_cell)))

        # Transfinite contorno exterior
        file.write('\n// Transfinite Outer Layer\n')
        file.write("Transfinite Curve {%i, %i, %i, %i, %i, %i, %i, %i, %i, %i, %i} = %i Using Progression %2.3f;\n" % (tuple(range(1101,1112))+ ((config.ol_cell + 1) * config.global_cell, config.ol_prog_cell)))

        # Transfinite contorno exterior
        file.write('\n// Transfinite Outer Domain\n')
        file.write("Transfinite Curve {%i, %i, %i, %i, %i, %i, %i} = %i Using Progression %2.3f;\n" % (1308, 1201, 1202, 1203, 1204, 1205, 1306, (config.domain_cell + 1) * config.global_cell, config.domain_prog_cell))

        # Transfinite Estela Perfil
        file.write('\n// Transfinite Airfoil Wake\n')
        if separation == True:
            file.write("Transfinite Curve {%i} = %i Using Progression 1;\n" % (11, 2))
            if config.bl == True:
                file.write("Transfinite Curve {%i} = %i Using Progression 1;\n" % (1307, (config.bl_cell + 1) * 2 + (config.ol_cell * config.global_cell + 1) * 2 - 2 ))
            else:
                file.write("Transfinite Curve {%i} = %i Using Progression 1;\n" % (1307, (config.ol_cell * config.global_cell +1 ) * 2))
        else:
            if config.bl == True:
                file.write("Transfinite Curve {%i} = %i Using Progression 1;\n" % (1307, (config.bl_cell +1) * 2 + (config.ol_cell * config.global_cell+ 1 ) * 2 - 3))
            else:
                file.write("Transfinite Curve {%i} = %i Using Progression 1;\n" % (1307, (config.ol_cell * config.global_cell + 1) * 2 - 1))

        # Definicion de las Physical Groups. No se pudo automatizar por tal caso se recomienda la version 4.5.6 del GMSH
        file.write('\n// Physical Groups\n')
        if config.bl == True:
            file.write("ids [] = Extrude {0, 0, -0.1} {Surface{1:28}; Layers {1} ; Recombine;};\n")
            file.write("""Physical Volume("Air") = {1:27};\n""")
            if separation == True:
                file.write("""Physical Surface("FrontandBack") = {1953, 1808, 1776, 1931, 1889, 1867, 1840, 1749, 1727, 1705, 1683, 1661, 1639, 1617, 1595, 1573, 1551, 1331, 1353, 1375, 1397, 1419, 1441, 1463, 1485, 1529, 1507, 24, 26, 25, 28, 27, 22, 23, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9};\n""")
                file.write("""Physical Surface("Inlet") = {1835, 1803};\n""")
                file.write("""Physical Surface("UpandDown") = {1771, 1948, 1876, 1862};\n""")
                file.write("""Physical Surface("Outlet") = {1952, 1906, 1888};\n""")
                file.write("""Physical Surface("Airfoil") = {1516, 1494, 1472, 1450, 1340, 1318, 1362, 1384, 1406, 1428, 1922};\n""")
            else:
                file.write("""Physical Surface("FrontandBack") = {23, 22, 28, 27, 26, 25, 24, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 1, 2, 3, 4, 5, 6, 7, 9, 8, 10, 1889, 1948, 1926, 1776, 1808, 1840, 1867, 1661, 1617, 1639, 1683, 1705, 1595, 1727, 1573, 1551, 1749, 1529, 1507, 1463, 1485, 1441, 1419, 1375, 1331, 1397, 1353};\n""")
                file.write("""Physical Surface("Inlet") = {1803, 1835};\n""")
                file.write("""Physical Surface("UpandDown") = {1943, 1771, 1876, 1862};\n""")
                file.write("""Physical Surface("Outlet") = {1947, 1905, 1888};\n""")
                file.write("""Physical Surface("Airfoil") = {1494, 1318, 1340, 1516, 1362, 1406, 1384, 1428, 1472, 1450};\n""")
            #file.write("""Physical Surface("FrontandBack") = {ids[{1:115:6, 128, 136, 144, 151, 157, 167, 60:114:6,120,127,128,135,143,150,156,166}],28};\n""") Metodo alternativo y automatico pero largo de realizar
        else:
            file.write("ids [] = Extrude {0, 0, -0.1} {Surface{1:18}; Layers {1} ; Recombine;};\n")
            file.write("""Physical Volume("Air") = {1:18};\n""")
            if separation == True:
                file.write("""Physical Surface("FrontandBack") = {13, 12, 18, 14, 15, 17, 16, 5, 1, 7, 9, 8, 2, 10, 6, 4, 3, 1620, 1669, 1588, 1701, 1647, 1723, 1556, 1529, 1485, 1441, 1463, 1507, 1331, 1353, 1375, 1397, 1419};\n""")
                file.write("""Physical Surface("Inlet") = {1583, 1615};\n""")
                file.write("""Physical Surface("UpandDown") = {1656, 1642, 1718, 1551};\n""")
                file.write("""Physical Surface("Outlet") = {1684, 1722, 1668};\n""")
                file.write("""Physical Surface("Airfoil") = {1450, 1472, 1494, 1428, 1516, 1318, 1340, 1362, 1384, 1406, 1696};\n""")
            else:
                file.write("""Physical Surface("FrontandBack") = {18, 12, 13, 14, 15, 16, 17, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 1620, 1588, 1718, 1556, 1696, 1669, 1647, 1529, 1485, 1507, 1441, 1463, 1419, 1397, 1375, 1353, 1331};\n""")
                file.write("""Physical Surface("Inlet") = {1615, 1583};\n""")
                file.write("""Physical Surface("UpandDown") = {1713, 1551, 1656, 1642};\n""")
                file.write("""Physical Surface("Outlet") = {1717, 1668, 1683};\n""")
                file.write("""Physical Surface("Airfoil") = {1494, 1472, 1450, 1428, 1406, 1340, 1362, 1384, 1318, 1516};\n""")
