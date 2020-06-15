# Datos del perfil
name='4415'
n_points=100
chord=1
separation=False
distribution='Cosine'

filename='NREL-S812.dat'
distribution='Double'
precision=6

# Estructura mallado perfil

hbl = 0.01
mesh_dirname = "mesh"
ang = 0

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
    # Ajuste de dirección de estela en grados - positivo sentido antihorario.
    adj_wake = 0

    #DEFINICION DEL MALLADO
    # Modifica globalmente el numero de celdas. Util para analisis de convergencia. No modifica valores en la capa limite.
    global_cell = 1.5
    # Numero de celdas sobre el perfil.
    airfoil_cell = 100
    # Numero de divisiones en la estela.
    wake_div_cell = 50
    # Progresion del espesor de las celdas de la estela. <1 mas celdas hacia el bf ; >1 mas celdas hacia el infinito.
    wake_prog_cell = 0.98
    # Numero de celdas en el contorno exterior.
    ol_cell = 20
    # Progresion del espesor de las celdas del contorno exterior. <1 mas celdas hacia el perfil ; >1 mas celdas hacia el infinito
    ol_prog_cell = 0.95
    # Numero de celdas dominio exterior
    domain_cell = 50
    # Progresion del espesor de las celdas del dominio. <1 mas celdas hacia el perfil ; >1 mas celdas hacia el infinito.
    domain_prog_cell = 1


    # CONFIGURACIÓN DE CAPA LIMITE. Sino se utiliza en el analisis ignorar esta parte.
    # Agregado de capa limite al analisis. True/False - (si/no).
    bl = True
    # Numero de celdas totales en la capa limite.
    bl_cell = 10
    # Altura de la primera celda de la capa limite. Se obtiene de determinar el y+ buscado.
    bl_first_cell = 0.002
    # Progresion de la longitud de la celdas de la capa limite. <1 decrece la altura ; >1 incrementa la altura
    bl_prog_cell = 1.2

    # CONFIGURACION PARA ALTOS ANGULOS DE ATAQUE
    # Altura Dominio interno en cuerdas de perfil a partir del eje x. Debe ser menor a "domain_height" y mayor al contorno exterior del perfil
    domain_int_height = 1
    # Densidad de celdas dominio interior - Celdas por unidad
    domain_int_dens_cell = 5
    # Densidad de celdas dominio exterior - Celdas por unidad
    domain_dens_cell = 2
