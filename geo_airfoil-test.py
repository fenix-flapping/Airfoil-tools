import math
from scipy.interpolate import interp1d
from NACA_4D import NACA_4D
from offset_airfoil import offset_airfoil
from found_division_index import found_division_index
import os
import numpy as np
import math
from scipy.interpolate import interp1d
from NACA_4D import NACA_4D
from offset_airfoil import offset_airfoil
from found_division_index import found_division_index
import os
import numpy as np
from config import *
from read_aorfoil import read_aorfoil

def apply_rotation(coords, angle, center=(0.25, 0)):
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

#Variables
max_angle=45
coords = NACA_4D('4415', n_points=100, chord=1, separation=True)
filename='NREL-S812.dat'
#coords=read_aorfoil('NREL-S812.dat', distribution='Cosine')
bl=True

# Valores de dominio
wake_long = 3 # Longitud de la estela en cuerdas de perfil a partir del BF
exp_porcent = 50 # Longitud de zona de expansion en porcentaje
tunnel_height = 2 # Altura del dominio en cuerdas de perfil a partir del eje x

# Buscar los indices donde se dividira el perfil 1 2/3 1/3 0, es necesario tener en cuenta la cuerda que se usa deberia ser una variable global
separation_point = coords.index(min(coords))




with open(os.path.join(mesh_dirname, "perfil.geo"), "w") as fid:
    # Rotacion de puntos del perfil
    coords_rotated = apply_rotation(coords, ang)

    # Determinacion de puntos de division
    break_points = found_division_index(coords, division)

    # Analisis de separacion de puntos de borde de fuga, se debe tener un tratamiento de la malla diferente segun sea el caso.
    if coords[0] == coords[len(coords) - 1]:
        separation = False
        coords_rotated.pop(-1)  # Eliminacion del ultimo punto repetido
    else:
        separation = True

    # Escritura de Puntos del perfil
    start_point = 1 # Inicio de numeracion de puntos y modificacion de puntos de division
    for i in range(len(break_points)):
        break_points[i] = break_points[i] + start_point
        
    count_point1 = start_point  # count1 es sumador de puntos del perfil
    fid.write('// Puntos del perfil\n')
    for x, y in coords_rotated:
        outputline = "Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point1, x, y)
        count_point1 = count_point1 + 1
        fid.write(outputline)

    # Escritura de Puntos del contorno exterior perfil
    count_point2 = 1000 + start_point # count_point2 es sumador de puntos de la capa limite, se alinea la numeracion de puntos
    # Calculo de puntos offset
    coords_offset_ob = offset_airfoil(coords, 0.05)
    coords_rotated = apply_rotation(coords_offset_ob, ang)
    fid.write('\n// Puntos del contorno exterior perfil\n')
    for x, y in coords_rotated:
        outputline = "Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point2, x, y)
        count_point2 = count_point2 + 1
        fid.write(outputline)

    # Escritura de Puntos de la capa limite
    if bl == True:
        count_point3 = 2000 + start_point # count_point3 es sumador de puntos de la capa limite, se alinea la numeracion de puntos
        # Calculo de puntos offset
        coords_offset_bl = offset_airfoil(coords, hbl)
        coords_rotated = apply_rotation(coords_offset_bl, ang)
        fid.write('\n// Puntos de la capa limite\n')
        for x, y in coords_rotated:
            outputline = "Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point3, x, y)
            count_point3 = count_point3 + 1
            fid.write(outputline)

    # Armado de lineas y splines (perfil, capa limite y contorno perfil)
    fid.write("\n// Lines and Splines\n")

    # Armado de Splines perfil
    count_line1 = 1  # count_line1 es sumador de lineas del perfil
    if separation == False:
        for i in range(len(break_points) - 2):
            fid.write("Spline(%i) = {%i:%i};\n" % (count_line1, break_points[i], break_points[i + 1]))
            count_line1 = count_line1 + 1
        i = i + 1
        fid.write("Spline(%i) = {%i:%i,%i};\n" % (count_line1, break_points[i], break_points[i + 1] - 1, start_point)) # Union con punto cero y cierre del perfil
        count_line1 = count_line1 + 1
    else:
        for i in range(len(break_points) - 1):
            fid.write("Spline(%i) = {%i:%i};\n" % (count_line1, break_points[i], break_points[i + 1]))
            count_line1 = count_line1 + 1

    # Armado de Splines del contorno exterior perfil
    count_line2 = 101  # count_line2 es sumador de lineas de la capa limite
    for i in range(len(break_points) - 1):
        fid.write("Line(%i) = {%i:%i};\n" % (count_line2, (break_points[i]) + 1000, (break_points[i + 1]) + 1000))
        count_line2 = count_line2 + 1

    # Armado de Splines capa limite
    if bl == True:
        count_line3 = 201 # count_line3 es sumador de lineas de la capa limite
        for i in range(len(break_points) - 1):
            fid.write("Spline(%i) = {%i:%i};\n" % (count_line3, (break_points[i]) + 2000, (break_points[i + 1]) + 2000))
            count_line3 = count_line3 + 1

    # Armado de lineas de division de corte
    count_line4 = 301  # count_line4 es sumador de lineas de corte de capa limite
    count_line5 = 401  # count_line5 es sumador de lineas de corte del contorno exterior perfil
    if bl == True:
        # Divisiones capa limite
        for i in range(len(break_points) - 1):
            fid.write("Line(%i) = {%i,%i};\n" % (count_line4, break_points[i], break_points[i] + 2000))
            count_line4 = count_line4 + 1
        if separation == False:
            i = i + 1
            fid.write("Line(%i) = {%i,%i};\n" % (count_line4, start_point , break_points[i] + 2000))
            count_line4 = count_line4 + 1
        else:
            i = i + 1
            fid.write("Line(%i) = {%i,%i};\n" % (count_line4, break_points[i], break_points[i] + 2000))
            count_line4 = count_line4 + 1
            fid.write("Line(%i) = {%i,%i};\n" % (count_line4, break_points[i], start_point)) 
            count_line4 = count_line4 + 1

        # Divisiones del contorno exterior perfil (con capa limite)
        for i in range(len(break_points)):
            fid.write("Line(%i) = {%i,%i};\n" % (count_line5, break_points[i] + 2000, break_points[i] + 1000))
            count_line5 = count_line5 + 1

    else:
        # Divisiones del contorno exterior perfil (sin capa limite)
        for i in range(len(break_points) - 1):
            fid.write("Line(%i) = {%i,%i};\n" % (count_line5, break_points[i], break_points[i] + 1000))
            count_line5 = count_line5 + 1
        if separation == False:
            i = i + 1
            fid.write("Line(%i) = {%i,%i};\n" % (count_line5, start_point , break_points[i] + 1000))
            count_line5 = count_line5 + 1
        else:
            i = i + 1
            fid.write("Line(%i) = {%i,%i};\n" % (count_line5, break_points[i], break_points[i] + 1000))
            count_line5 = count_line5 + 1
            fid.write("Line(%i) = {%i,%i};\n" % (count_line5, break_points[i], start_point))
            count_line5 = count_line5 + 1

    # Armado de Superficies del contorno del perfil
    count_sup1 = 1  # count_sup1 es sumador de superficies
    fid.write("\n// Surfaces\n")
    if bl == True:

        # Armado de Superficies en capa limite
        for i in range(len(break_points) - 1):
            fid.write("Line Loop(%i) = {%i, %i, %i, %i};\n" % (count_sup1, -(1 + i), 301 + i, 201 + i, -(302 + i)))
            fid.write("Plane Surface(%i) = {%i};\n" % (count_sup1, count_sup1))
            count_sup1 = count_sup1 + 1

        # Armado de Superficies en contorno exterior perfil (con capa limite)
        for i in range(len(break_points) - 1):
            fid.write("Line Loop(%i) = {%i, %i, %i, %i};\n" % (count_sup1, -(201 + i), 401 + i, 101 + i, -(402 + i)))
            fid.write("Plane Surface(%i) = {%i};\n" % (count_sup1, count_sup1))
            count_sup1 = count_sup1 + 1
    else:
        # Armado de Superficies en contorno exterior perfil (sin capa limite)
        for i in range(len(break_points) - 1):
            fid.write("Line Loop(%i) = {%i, %i, %i, %i};\n" % (count_sup1, -(1 + i), 401 + i, 101 + i, -(402 + i)))
            fid.write("Plane Surface(%i) = {%i};\n" % (count_sup1, count_sup1))
            count_sup1 = count_sup1 + 1

    # Transfinite y Recombine de Superficies del contorno del perfil
    fid.write("\n// Surfaces Transfinite and Recombine\n")
    for i in range(1, len(break_points)):
        fid.write(" Recombine Surface {%i};\n" % (i))
        fid.write(" Transfinite Surface {%i};\n" % (i))
    
    # Coordenadas de puntos de division del dominio
    break1 = break_points[int((len(break_points)-3)/2)] # Punto al 25% del extrados
    break2 = break_points[int((len(break_points))/2)] # Punto del borde de ataque
    break3 = break_points[int((len(break_points)+1)/2)] # Punto al 25% del intrados
        
    # Aramado de puntos del dominio
    fid.write("\n// Puntos del dominio\n")
    count_point4 = 3001 # count_point4 es sumador de puntos del dominio
    fid.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, wake_long + coords[0][0], tunnel_height))
    count_point4 = count_point4 + 1
    fid.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, ((wake_long * chord *exp_porcent)/100 + coords[0][0]), tunnel_height))
    count_point4 = count_point4 + 1
    fid.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, (coords[0][0]), tunnel_height))
    count_point4 = count_point4 + 1
    fid.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, (coords[break1 - start_point][0]), tunnel_height))
    count_point4 = count_point4 + 1
    fid.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, -tunnel_height, 0))
    count_point4 = count_point4 + 1
    fid.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, (coords[break3 - start_point][0]), -tunnel_height))
    count_point4 = count_point4 + 1
    fid.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, (coords[0][0]), -tunnel_height))
    count_point4 = count_point4 + 1
    fid.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, ((wake_long * chord *exp_porcent)/100 + coords[0][0]), -tunnel_height))
    count_point4 = count_point4 + 1
    fid.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, wake_long + coords[0][0], -tunnel_height))
    count_point4 = count_point4 + 1
    
    # Armado de Lineas del dominio
    fid.write("\n// Lineas del dominio\n")
    count_line6 = 501 # count10 de Lineas del dominio
    for i in range(1,4):
        fid.write("Line(%i) = {%i,%i};\n" % (count_line6, i + 3000, i + 3001))
        count_line6 = count_line6 + 1
    fid.write("Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count_point4, 0.25*chord, 0)) # Punto central del circulo frontal
    count_point4 = count_point4 + 1
    fid.write("Ellipse(%i) = {%i, %i, %i, %i};\n" % (count_line6, 3004 , count_point4 - 1, count_point4 - 1, 3005))
    count_line6 = count_line6 + 1
    fid.write("Ellipse(%i) = {%i, %i, %i, %i};\n" % (count_line6, 3005 , count_point4 - 1, count_point4 - 1, 3006))
    count_line6 = count_line6 + 1
    for i in range(6,9):
        fid.write("Line(%i) = {%i,%i};\n" % (count_line6, i + 3000, i + 3001))
        count_line6 = count_line6 + 1
    fid.write("Line(%i) = {%i,%i};\n" % (count_line6, 3009, 3001))
    
    # Armado de Lineas de Division del dominio
    if ang < max_angle:
        count_line7 = 601 # count_line7 de Lineas de Division del dominio
        fid.write("\n// Lineas de Division del dominio\n")
        fid.write("Line(%i) = {%i,%i};\n" % (count_line7, 3002, 3008))
        count_line7 = count_line7 + 1
        fid.write("Line(%i) = {%i,%i};\n" % (count_line7, 3003, 1000 + start_point))
        count_line7 = count_line7 + 1
        fid.write("Line(%i) = {%i,%i};\n" % (count_line7, 3004, break1 + 1000))
        count_line7 = count_line7 + 1
        fid.write("Line(%i) = {%i,%i};\n" % (count_line7, 3005, break2 + 1000))
        count_line7 = count_line7 + 1
        fid.write("Line(%i) = {%i,%i};\n" % (count_line7, 3006, break3 + 1000))
        count_line7 = count_line7 + 1
        fid.write("Line(%i) = {%i,%i};\n" % (count_line7, 3007, count_point2 - 1))
        count_line7 = count_line7 + 1
    
    # Armado de Superficies del dominio
    count_sup2 = 101 # count_sup2 sumador de Superficies del dominio
    
    if ang < max_angle:
        # Superfice estela
        fid.write("Line Loop(%i) = {%i, %i, %i, %i};\n" % (count_sup2, 508, 601, 501, 509))
        fid.write("Plane Surface(%i) = {%i};\n" % (count_sup2, count_sup2))
        count_sup2 = count_sup2 + 1
        
        # Superfice expansion de estela
        if bl == True:
            if separation == False:
                fid.write("Curve Loop(%i) = {%i, %i, %i, %i, %i, %i, %i, %i, %i};\n" % (count_sup2, 507, -601, 502, 602, -401, -301, count_line4 - 1, count_line5 - 1, -606))
                fid.write("Plane Surface(%i) = {%i};\n" % (count_sup2, count_sup2))
                count_sup2 = count_sup2 + 1
            else:
                fid.write("Line Loop(%i) = {%i, %i, %i, %i, %i, %i, %i, %i, %i, %i};\n" % (count_sup2, 507, -601, 502, 602, -401, -301, -(count_line4 - 1), count_line4 - 2, count_line5 - 1, -606))
                fid.write("Plane Surface(%i) = {%i};\n" % (count_sup2, count_sup2))
                count_sup2 = count_sup2 + 1
        else:
            if separation == False:
                fid.write("Curve Loop(%i) = {%i, %i, %i, %i, %i, %i, %i};\n" % (count_sup2, 507, -601, 502, 602, -401, count_line5 - 1, -606))
                fid.write("Plane Surface(%i) = {%i};\n" % (count_sup2, count_sup2))
                count_sup2 = count_sup2 + 1
            else:
                fid.write("Line Loop(%i) = {%i, %i, %i, %i, %i, %i, %i, %i};\n" % (count_sup2, 507, -601, 502, 602, -401, -(count_line5 - 1), count_line5 - 2, -606))
                fid.write("Plane Surface(%i) = {%i};\n" % (count_sup2, count_sup2))
                count_sup2 = count_sup2 + 1
    else:
        None #armar para angulos de ataque elevados
        #Curve Loop(103) = {107, 108, -409, -309, 310, 301, 401, 101, 102, 103, 104, 105, 106};
                
                
                
def write_perfil(coords, lc=0.002, mesh_dirname="mesh", bl=True):
    with open(os.path.join(mesh_dirname, "perfil.geo"),"w") as fid:  # devuelve el path del directorio de donde se ejecuta
        fid.write("lc = %f;\n" % (lc))  # escribe mh6_lc = 0.002;
        startpoint = 0
        endpoint = len(coords) - 1
        midpoint = int(startpoint + 0.5 * (endpoint - startpoint))
        fid.write("perfilStartpoint = %i;\n" % startpoint)
        fid.write("perfilMidpoint = %i;\n" % midpoint)
        fid.write("perfilEndpoint = %i;\n" % endpoint)
        j = startpoint
        for x, y in coords:
            outputline = "Point(%i) = { %8.8f, %8.8f, 0.0, lc};\n" % (j, x, y)
            j = j + 1
            fid.write(outputline)

    if bl:

        coords_offset = offset_coords(coords)
        with open(os.path.join(mesh_dirname, "perfil_bl.geo"), "w") as fid:
            startpoint = j
            endpoint = startpoint + len(coords_offset) - 1
            midpoint = int(startpoint + 0.5 * (endpoint - startpoint))
            fid.write("blStartpoint = %i;\n" % startpoint)
            fid.write("blMidpoint = %i;\n" % midpoint)
            fid.write("blEndpoint = %i;\n" % endpoint)
            for x, y in coords_offset:
                outputline = "Point(%i) = { %8.8f, %8.8f, 0.0, lc };\n" % (j, x, y)
                j = j + 1
                fid.write(outputline)


def write_geo(output_filename, coords_rotated, lc=0.005, largo=10, alto=8):
    lc_name = "%s_lc" % output_filename[0:3]
    ancho = 1  # longitud del extrudado de la malla 2D
    startpoint = 1000
    with open(output_filename, "w") as fid:
        fid.write("%s = %f;\n" % (lc_name, lc))
        j = startpoint
        for x, y in coords_rotated:  # Armado de puntos y spline final de gmsh
            outputline = "Point(%i) = { %8.8f, %8.8f, 0.0, %s};\n" % (j, x, y, lc_name)
            j = j + 1
            fid.write(outputline)
        fid.write("Spline(%i) = {%i:%i,%i};\n" % (startpoint, startpoint, j, startpoint))
        k = j + 1
        j = j + 1
        fid.write("//+\n")
        fid.write("Point(%i) = {-%1.4f, -%1.4f, 0, %1.4f};\n" % (j, 0.4 * largo, 0.5 * alto, ancho));
        j = j + 1
        fid.write("Point(%i) = {%1.4f, -%1.4f, 0, %1.4f};\n" % (j, (1 - 0.4) * largo, 0.5 * alto, ancho));
        j = j + 1
        fid.write("Point(%i) = {%1.4f, %1.4f, 0, %1.4f};\n" % (j, (1 - 0.4) * largo, 0.5 * alto, ancho));
        j = j + 1
        fid.write("Point(%i) = {-%1.4f, %1.4f, 0, %1.4f};\n" % (j, 0.4 * largo, 0.5 * alto, ancho))
        fid.write("Line(%i) = {%i, %i};\n" % (startpoint + 1, k, k + 1))
        fid.write("Line(%i) = {%i, %i};\n" % (startpoint + 2, k + 1, k + 2))
        fid.write("Line(%i) = {%i, %i};\n" % (startpoint + 3, k + 2, k + 3))
        fid.write("Line(%i) = {%i, %i};\n" % (startpoint + 4, k + 3, k))
        fid.write("Line Loop(1) = {%i, %i, %i, %i};\n" % tuple(range(startpoint + 1, startpoint + 5)))
        fid.write("Line Loop(2) = {%i};\n" % startpoint)
        fid.write("""Surface(10) = {1, 2};
    TwoDimSurf = 10;
    Recombine Surface{TwoDimSurf};

    ids[] = Extrude {0, 0, 1}
    {
        Surface{TwoDimSurf};
        Layers{1};
        Recombine;
    };

    Physical Surface("outlet") = {ids[3]};
    Physical Surface("topAndBottom") = {ids[{2, 4}]};
    Physical Surface("inlet") = {ids[5]};
    Physical Surface("airfoil") = {ids[{6:8}]};
    Physical Surface("frontAndBack") = {ids[0], TwoDimSurf};
    Physical Volume("volume") = {ids[1]};""")


def write_box(alto, largo, mesh_dirname="mesh"):
    ancho = 0.5
    startpoint = 1000
    j = startpoint
    with open(os.path.join(mesh_dirname, "box.geo"), "w") as fid:
        fid.write("Point(%i) = {-%1.4f, -%1.4f, 0, %1.4f};\n" % (j, 0.4 * largo, 0.5 * alto, ancho));
        j = j + 1
        fid.write("Point(%i) = {%1.4f, -%1.4f, 0, %1.4f};\n" % (j, (1 - 0.4) * largo, 0.5 * alto, ancho));
        j = j + 1
        fid.write("Point(%i) = {%1.4f, %1.4f, 0, %1.4f};\n" % (j, (1 - 0.4) * largo, 0.5 * alto, ancho));
        j = j + 1
        fid.write("Point(%i) = {-%1.4f, %1.4f, 0, %1.4f};\n" % (j, 0.4 * largo, 0.5 * alto, ancho))
        fid.write("Line(%i) = {%i, %i};\n" % (startpoint, startpoint, startpoint + 1))
        fid.write("Line(%i) = {%i, %i};\n" % (startpoint + 1, startpoint + 1, startpoint + 2))
        fid.write("Line(%i) = {%i, %i};\n" % (startpoint + 2, startpoint + 2, startpoint + 3))
        fid.write("Line(%i) = {%i, %i};\n" % (startpoint + 3, startpoint + 3, startpoint))
        fid.write("Line Loop(3) = {%i, %i, %i, %i};\n" % tuple(range(startpoint, startpoint + 4)))
