
def read_airfoil(filename):
    ignore_head=0 # Elimina el titulo del archivo .dat
    coords = []
    with open(filename, "r") as file:
        for line in file.readlines()[ignore_head:]:
            data = line.split()
            coords.append((float(data[0]), float(data[1])))

    return coords
