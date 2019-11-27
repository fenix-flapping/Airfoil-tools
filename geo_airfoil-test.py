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


def read_aorfoil(filename):
    ignore_head = 0
    coords = []
    with open(filename, "r") as fid:
        for line in fid.readlines()[ignore_head:]:
            data = line.split()
            coords.append((float(data[0]), float(data[1])))

    # Se asegura de que el punto inicial este repetido al final de la secuencia
    #    if coords[0] != coords[-1]:
    #        coords.append(coords[0])

def read_aorfoil(filename):
    ignore_head = 0
    coords = []
    with open(filename, "r") as fid:
        for line in fid.readlines()[ignore_head:]:
            data = line.split()
            coords.append((float(data[0]), float(data[1])))

    # Se asegura de que el punto inicial este repetido al final de la secuencia
    #    if coords[0] != coords[-1]:
    #        coords.append(coords[0])
    return coords


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


chord = 1
#coords = NACA_4D('0012', chord, 150, separation=True)
coords=read_aorfoil('NREL-S812.dat')

# Buscar los indices donde se dividira el perfil 1 2/3 1/3 0, es necesario tener en cuenta la cuerda que se usa deberia ser una variable global
separation_point = coords.index(min(coords))
division = [2 / 3 * chord, 1 / 3 * chord, 0.1 * chord, 0.01 * chord]
hbl = 0.01
mesh_dirname = "mesh"
bl = False
ang = 0

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
    count1 = start_point  # count1 es sumador de puntos del perfil
    fid.write('// Puntos del perfil\n')
    for x, y in coords_rotated:
        outputline = "Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count1, x, y)
        count1 = count1 + 1
        fid.write(outputline)

    # Escritura de Puntos del contorno exterior perfil
    count2 = 1000 + start_point # count2 es sumador de puntos de la capa limite, se alinea la numeracion de puntos
    # Calculo de puntos offset
    coords_offset = offset_airfoil(coords, 0.1)
    coords_rotated = apply_rotation(coords_offset, ang)
    fid.write('\n// Puntos del contorno exterior perfil\n')
    for x, y in coords_rotated:
        outputline = "Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count2, x, y)
        count2 = count2 + 1
        fid.write(outputline)

    # Escritura de Puntos de la capa limite
    if bl == True:
        count3 = 2000 + start_point # count3 es sumador de puntos de la capa limite, se alinea la numeracion de puntos
        # Calculo de puntos offset
        coords_offset = offset_airfoil(coords, hbl)
        coords_rotated = apply_rotation(coords_offset, ang)
        fid.write('\n// Puntos de la capa limite\n')
        for x, y in coords_rotated:  # Armado de puntos y spline final de gmsh
            outputline = "Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (count3, x, y)
            count3 = count3 + 1
            fid.write(outputline)

    # Armado de lineas y splines
    fid.write("\n// Lines and Splines\n")

    # Armado de Splines perfil
    count4 = 1  # count4 es sumador de lineas del perfil
    if separation == False:
        for i in range(len(break_points) - 2):
            fid.write("Spline(%i) = {%i:%i};\n" % (count4, break_points[i], break_points[i + 1]))
            count4 = count4 + 1
        i = i +1
        fid.write("Spline(%i) = {%i:%i,%i};\n" % (count4, break_points[i], break_points[i + 1] - 1, start_point))
        count4 = count4 + 1
    else:
        for i in range(len(break_points) - 1):
            fid.write("Spline(%i) = {%i:%i};\n" % (count4, break_points[i], break_points[i + 1]))
            count4 = count4 + 1

    # Armado de Splines del contorno exterior perfil
    count5 = 101  # count5 es sumador de lineas de la capa limite
    for i in range(len(break_points) - 1):
        fid.write("Line(%i) = {%i:%i};\n" % (count5, (break_points[i]) + 1000, (break_points[i + 1]) + 1000))
        count5 = count5 + 1

    # Armado de Splines capa limite
    if bl == True:
        count6 = 201 # count6 es sumador de lineas de la capa limite
        for i in range(len(break_points) - 1):
            fid.write("Spline(%i) = {%i:%i};\n" % (count6, (break_points[i]) + 2000, (break_points[i + 1]) + 2000))
            count6 = count6 + 1

    # Armado de lineas de division de corte
    count7 = 301  # count7 es sumador de lineas de corte de capa limite
    count8 = 401  # count7 es sumador de lineas de corte del contorno exterior perfil
    if bl == True:
        # Divisiones capa limite
        for i in range(len(break_points) - 1):
            fid.write("Line(%i) = {%i,%i};\n" % (count7, break_points[i], break_points[i] + 2000))
            count7 = count7 + 1
        if separation == False:
            i = i + 1
            fid.write("Line(%i) = {%i,%i};\n" % (count7, start_point , break_points[i] + 2000))
            count7 = count7 + 1
        else:
            i = i + 1
            fid.write("Line(%i) = {%i,%i};\n" % (count7, break_points[i], break_points[i] + 2000))
            count7 = count7 + 1
            fid.write("Line(%i) = {%i,%i};\n" % (count7, break_points[i], start_point))
            count7 = count7 + 1

        # Divisiones del contorno exterior perfil (con capa limite)
        for i in range(len(break_points)):
            fid.write("Line(%i) = {%i,%i};\n" % (count8, break_points[i] + 2000, break_points[i] + 1000))
            count8 = count8 + 1

    else:
        # Divisiones del contorno exterior perfil (sin capa limite)
        for i in range(len(break_points) - 1):
            fid.write("Line(%i) = {%i,%i};\n" % (count8, break_points[i], break_points[i] + 1000))
            count8 = count8 + 1
        if separation == False:
            i = i + 1
            fid.write("Line(%i) = {%i,%i};\n" % (count8, start_point , break_points[i] + 1000))
            count7 = count8 + 1
        else:
            i = i + 1
            fid.write("Line(%i) = {%i,%i};\n" % (count8, break_points[i], break_points[i] + 1000))
            count8 = count8 + 1
            fid.write("Line(%i) = {%i,%i};\n" % (count8, break_points[i], start_point))
            count8 = count8 + 1

    # Armado de Superficies
    count8 = 1  # count8 es sumador de superficies
    fid.write("\n// Surfaces\n")
    if bl == True:

        # Armado de Superficies en capa limite
        for i in range(len(break_points) - 1):
            fid.write("Line Loop(%i) = {%i, %i, %i, %i};\n" % (count8, -(1 + i), 301 + i, 201 + i, -(302 + i)))
            fid.write("Surface(%i) = {%i};\n" % (count8, count8))
            count8 = count8 + 1

        # Armado de Superficies en contorno exterior perfil
        for i in range(len(break_points) - 1):
            fid.write("Line Loop(%i) = {%i, %i, %i, %i};\n" % (count8, -(201 + i), 401 + i, 101 + i, -(402 + i)))
            fid.write("Surface(%i) = {%i};\n" % (count8, count8))
            count8 = count8 + 1
    else:
        # Armado de Superficies en contorno exterior perfil
        for i in range(len(break_points) - 1):
            fid.write("Line Loop(%i) = {%i, %i, %i, %i};\n" % (count8, -(1 + i), 401 + i, 101 + i, -(402 + i)))
            fid.write("Surface(%i) = {%i};\n" % (count8, count8))
            count8 = count8 + 1

    # Transfinite y Recombine de Superficies
    fid.write("\n// Surfaces Transfinite and Recombine\n")
    for i in range(1, len(break_points)):
        fid.write(" Recombine Surface {%i};\n" % (i))
        fid.write(" Transfinite Surface {%i};\n" % (i))


def write_perfil(coords, lc=0.002, mesh_dirname="mesh", bl=True):
    with open(os.path.join(mesh_dirname, "perfil.geo"),
              "w") as fid:  # devuelve el path del directorio de donde se ejecuta
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
