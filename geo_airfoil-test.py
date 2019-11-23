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
    return coords

def apply_rotation(coords, angle, center=(0.25,0)):
    center = np.array(center)
    theta = np.radians(angle) #convierte en radianes los gradosº
    c, s = np.cos(theta), np.sin(theta) # asigna valores a mas de una variable con la coma
    R = np.array(((c,-s), (s, c))).T # Transpuesta de la matriz
    coords_rotated = []
    for point in coords:
        vector = point - center
        vector_rotated = R.dot(vector) #Producto vectorial de matriz de rotacion con vector de cada coordenada
        coords_rotated.append(tuple(vector_rotated + center)) # calculo rotacion del perfil
    return coords_rotated

chord=1
#coords=NACA_4D('2412',chord,300)
coords=read_aorfoil('NREL-S812.dat')

# Buscar los indices donde se dividira el perfil 1 2/3 1/3 0, es necesario tener en cuenta la cuerda que se usa deberia ser una variable global
separation_point=coords.index(min(coords))
division=[2/3*chord , 1/3*chord, 0.1*chord]

mesh_dirname="mesh"
bl=True
ang=30

with open(os.path.join(mesh_dirname, "perfil.geo"), "w") as fid:
    j = 0 # j es sumador de puntos
    # Escritura de Puntos del perfil con precision 000.000000
    coords_rotated=apply_rotation(coords, ang)
    fid.write('// Puntos del perfil\n')
    for x, y in coords_rotated: # Armado de puntos y spline final de gmsh
        outputline = "Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (j, x, y)
        j = j + 1
        fid.write(outputline)

    # Escritura de Puntos de la capa limite
    if bl==True:
        fid.write('\n// Puntos de la capa limite\n')
        coords_offset=offset_airfoil(coords,0.01)
        coords_rotated=apply_rotation(coords_offset, ang)
        for x, y in coords_rotated: # Armado de puntos y spline final de gmsh
            outputline = "Point(%i) = { %3.6f, %3.6f, 0.0};\n" % (j, x, y)
            j = j + 1
            fid.write(outputline)
    
    # Armado de lineas y splines {%i:%i,%i}
    k=1 # k es sumador de lineas y splines
    break_points=found_division_index(coords, division)
    fid.write("\n// Lines and Splines\n")
    for i in range(len(break_points)-1):
        fid.write("Line(%i) = {%i:%i};\n" % (k, break_points[i], break_points[i+1]))
        k=k+1
        fid.write("Line(%i) = {%i:%i};\n" % (k, break_points[i] + len(coords), break_points[i+1] + len(coords)))
        k=k+1
        fid.write("Line(%i) = {%i,%i};\n" % (k, break_points[i], break_points[i] + len(coords)))
        k = k + 1
    fid.write("Line(%i) = {%i,%i};\n" % (k+2, break_points[i+1], break_points[i+1] + len(coords)))

    # Armado de Superficies y transfinite y recombine de estas
    l = 1  # k es sumador de lineas y splines
    fid.write("\n// Surfaces\n")
    for i in range(len(break_points) - 1):
        fid.write("Line Loop(%i) = {%i, %i, %i, %i};\n" % (i+1,-l,(l+2),(l+1),-(l+5)))
        fid.write("Surface(%i) = {%i};\n" % (i+1,i+1))
        l = l + 3
        
    # Transfinite y Recombine de Superficies
    fid.write("\n// Surfaces Transfinite and Recombine\n")
    for i in range(1,len(break_points)):
        fid.write(" Recombine Surface {%i};\n" % (i))
        fid.write(" Transfinite Surface {%i};\n" %(i))
    
    
def write_perfil(coords, lc=0.002, mesh_dirname="mesh", bl=True):
    with open(os.path.join(mesh_dirname, "perfil.geo"), "w") as fid: # devuelve el path del directorio de donde se ejecuta
        fid.write("lc = %f;\n" % (lc)) # escribe mh6_lc = 0.002;
        startpoint = 0
        endpoint = len(coords)-1
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
            endpoint = startpoint+len(coords_offset)-1
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
    ancho = 1 # longitud del extrudado de la malla 2D
    startpoint = 1000
    with open(output_filename, "w") as fid:
        fid.write("%s = %f;\n" % (lc_name, lc))
        j = startpoint
        for x, y in coords_rotated: # Armado de puntos y spline final de gmsh
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


