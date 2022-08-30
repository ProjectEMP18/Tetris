import random
import os
def lectura_de_rotaciones():
    piezas  = []

    with open("piezas.txt") as archivo:
        for linea in archivo:
            pieza = []
            linea = linea.rstrip("\n")
            linea , piezas_a_eliminar = linea.split(" # ")
            linea = linea.split(" ")
            for posicion in linea:
                posicion_de_pieza= []
                celdas = posicion.split(";")
                for celda in celdas:
                    lista_celda = []
                    celda = celda.rstrip(")")
                    celda = celda.lstrip("(")
                    celda = celda.split(",")
                    for coordenada in celda:
                        coordenada = int(coordenada)
                        lista_celda.append(coordenada)
                    lista_celda= tuple(lista_celda)
                    posicion_de_pieza.append(lista_celda)
                posicion_de_pieza = tuple(posicion_de_pieza)
                pieza.append(posicion_de_pieza)
            piezas.append(pieza)
    
    return piezas

def piezas_nuevo():
    piezas_total  = lectura_de_rotaciones()
    piezas = []
    for pieza in piezas_total:
        piezas.append(pieza[0])
    return tuple(piezas)

PARTIDA = "partida.txt"
PUNTAJE = 0
OCUPADA = "c"
ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6
"""
PIEZAS = (
    ((0, 0), (1, 0), (0, 1), (1, 1)), # Cubo
    ((0, 0), (1, 0), (1, 1), (2, 1)), # Z (zig-zag)
    ((0, 0), (0, 1), (1, 1), (1, 2)), # S (-Z)
    ((0, 0), (0, 1), (0, 2), (0, 3)), # I (línea)
    ((0, 0), (0, 1), (0, 2), (1, 2)), # L
    ((0, 0), (1, 0), (2, 0), (2, 1)), # -L
    ((0, 0), (1, 0), (2, 0), (1, 1)), # T
)
"""
ROTACIONES = lectura_de_rotaciones()
PIEZAS = piezas_nuevo()

def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    if pieza != None:
        return PIEZAS[pieza]
    else:
        pieza_nueva = random.choice(PIEZAS)
        return pieza_nueva

def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y).
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    pieza_a_trasladar = list(pieza)
    pieza_trasladada = []
    for parte in pieza_a_trasladar:
        coordenadas = []
        parte = list(parte)
        coordenadas = [parte[0]+ dx, parte[1] + dy]
        pieza_trasladada.append(tuple(coordenadas))

    return tuple(pieza_trasladada)

def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de
    sus posiciones superiores es 0 (cero).
    """
    grilla = []

    for _ in range (ALTO_JUEGO):
        fila =[]
        for _ in range(ANCHO_JUEGO):
            fila.append(None)

        grilla.append(fila)

    pieza_centrada = list(trasladar_pieza(pieza_inicial, ANCHO_JUEGO//2 ,0))
    pieza_final = []
    for cell in pieza_centrada:
        cell_final = list(cell)
        pieza_final.append(cell_final)

    for celda_01 in pieza_final:
        celda_def = celda_01
        y = celda_def[1]
        x = celda_def[0]
        grilla[y][x] = celda_def

    return grilla

def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    dimension = (len(juego[0]), len(juego))
    return dimension

def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina
    superior izquierda de la grilla.
    """
    pieza_cayendo = []
    pieza_cayendo_y= []

    for numero_fila in range(len(juego)):
        
        for numero_columna in range(len(juego[numero_fila])):
            if juego[numero_fila][numero_columna] != OCUPADA and juego[numero_fila][numero_columna] != None:
                pieza_cayendo_y = []
                pieza_cayendo_y.append(numero_columna)
                pieza_cayendo_y.append(numero_fila)
                pieza_cayendo.append(tuple(pieza_cayendo_y))

    return tuple(pieza_cayendo)

def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.

    La coordenada (0, 0) se refiere a la posición que está en la esquina
    superior izquierda de la grilla.
    """
    return juego[y][x] == OCUPADA

def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """

    pieza_sin_mover = list(pieza_actual(juego))
    pieza_sin_mover_def = pasar_a_lista(pieza_sin_mover)

    pieza_movida = list(trasladar_pieza(pieza_actual(juego),direccion, 0))
    pieza_movida_def = pasar_a_lista(pieza_movida)

    ancho, alto = dimensiones(juego)
    comprobador = None
    for parte in pieza_sin_mover_def:
        x , y = parte

        if (0<= (x+direccion) <= ancho-1) and juego[y][(x+direccion)] != OCUPADA:
            comprobador = True
            
        else:
            comprobador = False
            break

    if comprobador == True:
        for parte_2 in pieza_sin_mover_def:
            x , y = parte_2
            juego[y][x] = None
        for parte_3 in pieza_movida_def:
            x, y = parte_3
            juego[y][x] = parte_3
        return juego
    else:
        return juego

def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.

    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).

    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar
    completamente en la grilla para poder seguir jugando, si al intentar
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada,
    se debe devolver el mismo juego que se recibió.
    """
    vol = False
    
    ancho, alto =dimensiones(juego)
    pieza = pieza_actual(juego)
    pieza_def = pasar_a_lista(pieza)

    juego = eliminar_filas(juego)
    for celda in pieza_def:
        x,y = celda
        if y == (alto-1):
            vol = True
            break
    if vol == True:
        for celda in pieza_def:
            x,y = celda
            juego[y][x] = OCUPADA
        pieza_def = pasar_a_lista(trasladar_pieza(siguiente_pieza,ancho//2,0))
        for celda in pieza_def:
            x,y = celda
            juego[y][x]= celda
        juego = eliminar_filas(juego)
        return (juego, True)

    for celda in pieza_def:
        x, y =  celda
        if juego[y+1][x]== OCUPADA:
            for celda in pieza_def:
                x,y = celda
                juego[y][x] = OCUPADA

            pieza_def = pasar_a_lista(trasladar_pieza(siguiente_pieza,ancho//2,0))
            for celda in pieza_def:
                x,y = celda
                juego[y][x]= celda
            juego = eliminar_filas(juego)
            if terminado(juego):
                return(juego,False)
            return (juego, True)

    for parte in pieza_def:
        x, y = parte
        juego[y][x] = None
    
    pieza_final = trasladar_pieza(pieza, 0, 1)
    pieza_final_def = pasar_a_lista(pieza_final)
    for parte in pieza_final_def:
        x, y = parte
        juego[y][x]= parte
    return (juego, False)

def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    for x in juego[0]:
        if x == OCUPADA:
            return True
    return False

def posicion_valida(pieza, juego):
    ancho, alto = dimensiones(juego)
    for x, y in pieza:
        if 0 <= x < ancho and 0<= y < alto and juego[y][x] == None:
            continue
        return False
    return True

def eliminar_filas (juego):
    ancho, alto = dimensiones(juego)
    contador_final = 0
    for fila_final in juego:
        contador_celda = 0
        for celda in fila_final:
            if celda == OCUPADA:
                contador_celda += 1
        if contador_celda == ancho:
            juego.pop(contador_final)
            juego.insert(0,[None]*ancho)
            contador_final += 1
            continue
        contador_final += 1

    return juego

def pasar_a_lista(tupla_de_tuplas):
    pieza_def = []
    for celda in tupla_de_tuplas:
        celda_def = list(celda)
        pieza_def.append(celda_def)
    return pieza_def

def buscar_rotación(pieza_en_origen):
    for pieza in ROTACIONES:
        if pieza_en_origen in pieza:
            indice = pieza.index(pieza_en_origen)
            if 0<= indice+1 < len(pieza):
                return (pieza[indice+1])
            else:
                indice = 0
                return (pieza[0])

def rotar(juego):
    ancho, alto= dimensiones(juego)
    pieza_a_rotar = pieza_actual(juego)
    pieza_ordenada = sorted(pieza_a_rotar)
    primera_posicion = pieza_ordenada[0]
    dx , dy = primera_posicion
    pieza_en_origen = trasladar_pieza(pieza_ordenada, -dx, -dy)
    siguiente_rotación = buscar_rotación(pieza_en_origen)
    pieza_rotada = trasladar_pieza(siguiente_rotación, dx, dy)
    for celda in pieza_a_rotar:
        x, y = celda
        juego[y][x]= None
    
    pieza_rotada_aux = sorted(pieza_rotada)
    if posicion_valida(pieza_rotada_aux, juego):
        for celda in pieza_rotada:
            x, y = celda
            juego[y][x]= celda
        return juego
    else:
        pieza_rotada = trasladar_pieza(pieza_rotada,-1, 0)
        while not posicion_valida(pieza_rotada,juego):
            pieza_rotada = trasladar_pieza(pieza_rotada,-1,0)
        for celda in pieza_rotada:
            x, y = celda
            juego[y][x] = celda
        return juego

def gurdar_juego(juego, puntos):
    """
    Guarda la partida actual en un archivo txt
    """
    with open(PARTIDA, "w") as archivo:
        puntaje = str(puntos)
        archivo.write(puntaje)
        archivo.write("\n")
        for fila in juego:
            fila_1 = ""
            contador_celdas = 0
            for celda in fila:
                contador_celdas += 1
                if contador_celdas == ANCHO_JUEGO-1:
                    celda = str(celda)
                celda = str(celda)+";"
                fila_1 += celda
            fila = str(fila_1)
            archivo.write(fila)
            archivo.write("\n")

def cargar_partida ():
    """
    Si es que hay una partida anterior guardada la carga
    """
    if os.path.isfile(PARTIDA):
        contador_fila_archivo = 0
        puntos = 0
        juego = []
        fila = []
        elementos = []
        numero= []
        contador = 0
        with open(PARTIDA) as archivo:
            for linea in archivo:
                if contador_fila_archivo == 0:
                    linea = linea.rstrip("\n")
                    puntos = int(linea)
                    contador_fila_archivo += 1
                else:
                    fila = []
                    linea=linea.rstrip("\n")
                    linea= linea.rstrip(";")
                    fila = linea.split(";")
                    for elemento in fila:
                        elemento = str(elemento)
                        if elemento == "None":
                            fila[contador] = None
                        elif elemento != OCUPADA:
                            elemento = elemento.lstrip("[")
                            elemento = elemento.rstrip("]")
                            elemento = elemento.strip()
                            elemento = elemento.split(",")
                            contador_tupla = 0
                            for e in elemento:
                                elemento[contador_tupla] = int(e)
                                contador_tupla += 1
                            fila[contador] = elemento
                
                        contador+= 1
                    contador = 0
            
                    juego.append(fila)
                    contador_fila_archivo += 1

        return (juego, puntos)