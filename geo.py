


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


def write_perfil(coords, lc=0.002, mesh_dirname="mesh", bl=True):
    with open(os.path.join(mesh_dirname, "perfil.geo"), "w") as fid:
        fid.write("lc = %f;\n" % (lc))
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
