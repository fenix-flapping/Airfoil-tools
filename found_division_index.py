'''
Funcion que busca valores especificos de la ordenada del extrados e intrados
y devuelve el indice en que se ubica del vector de coordenadas del perfil.
No posee proteccion ante pedido de valores erroneos o fuera de escala
'''
def found_division_index(coords , division):
    point_division_extr= [0] # El primer punto es siempre el "0"
    point_division_intr = [len(coords)-1]
    for div in division:
        j=0
        k=0
        for i in range(len(coords)):
            if coords[i][0]<div and j==0:
                divextr=i
                j=1
            if coords[-i][0]<div and k==0:
                divintr=len(coords)-i
                k=1
            if j==1 and k==1:
                break
        point_division_extr.append(divextr)
        point_division_intr.append(divintr)
    # El primer punto del intrados es el valor minimo del vector de coordenadas del perfil
    point_division_intr.append(coords.index(min(coords))) 
    point_division=point_division_extr[:]+point_division_intr[::-1]
    return point_division



 