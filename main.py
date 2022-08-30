import tetris
import gamelib
import os

def leer_teclas():
    dicc = {}
    with open ("teclas.txt") as archivo:
        lineas = archivo.readlines()
    for clave_y_valor in lineas:
        if clave_y_valor != "\n":
            clave_y_valor = clave_y_valor.rstrip("\n")
            tecla_y_valor = clave_y_valor.split(" = ")
            tecla_y_valor[1] = tecla_y_valor[1]
            dicc[tecla_y_valor[0]] = tecla_y_valor[1]
        else:
            continue
    return dicc

ALTO_VENTANA = 900
ANCHO_VENTANA = 800
PARTIDA = "partida.txt"
ARCHIVO_DE_PUNTAJES = "puntajes.txt"
CELDA_DE_GRILLA = 50
ESPERA_DESCENDER = 8
TECLAS = leer_teclas()

def main():
    # Inicializar el estado del juego
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    pieza_inicial = tetris.generar_pieza()
    juego = tetris.crear_juego(pieza_inicial)
    pieza_siguiente = tetris.generar_pieza()
    puntos = 0
    escribio_nombre= False
    timer_bajar = ESPERA_DESCENDER
    while gamelib.loop(fps=30):

        gamelib.draw_begin()
        # Dibujar la pantalla
        juego_mostrar(juego,puntos, pieza_siguiente)
        gamelib.draw_end()

        for event in gamelib.get_events():
          if not event:
              break
          if event.type == gamelib.EventType.KeyPress and event.key == "Escape":
              return
          if event.type == gamelib.EventType.KeyPress:
              tecla = event.key
              juego, cambio_de_pieza, puntos =juego_actualizar (juego, puntos, tecla, pieza_siguiente)

              # Actualizar el juego, según la tecla presionada
        
        timer_bajar -= 1
        if timer_bajar == 0:
            timer_bajar = ESPERA_DESCENDER
            # Descender la pieza automáticamente
            juego, cambio_de_pieza =tetris.avanzar(juego, pieza_siguiente)
            if cambio_de_pieza == True:
                pieza_siguiente = tetris.generar_pieza()
            if not tetris.terminado(juego):
                puntos += 5
            elif verificar_top_10(puntos)== True and tetris.terminado(juego) and escribio_nombre == False:
                nombre = gamelib.input("Ingrese sus iniciales:")
                guardar_high_score(puntos,nombre)
                mostrar_high_score()
                escribio_nombre= True
            if tetris.terminado(juego) and verificar_top_10(puntos)==False and escribio_nombre== False:
                mostrar_high_score()
                escribio_nombre=True
            
def crear_grilla(ancho, alto):
    """
    Crea la grilla
    """
    gamelib.draw_rectangle(0,0,450,ALTO_VENTANA, outline = "red", fill = "grey")
    distancia_x = 450// ancho
    distancia_y = ALTO_VENTANA// alto
    for i in range(ancho):
        gamelib.draw_line((i*distancia_x),0,(distancia_x*i),ALTO_VENTANA,fill = "red", width = 2)

    for j in range(alto):
        gamelib.draw_line(0,(j*distancia_y),450,(j*distancia_y),fill = "red", width = 2)

def representar_pieza(pieza_actual, ancho, alto):
    """
    Representa la pieza actual en la grilla
    """
    distancia_x = 450// ancho
    distancia_y = ALTO_VENTANA// alto
    for celda in pieza_actual:
        x,y = celda
        gamelib.draw_rectangle((x*distancia_x),(y*distancia_y),(x*distancia_x)+CELDA_DE_GRILLA, (y*distancia_y)+CELDA_DE_GRILLA,outline= "black", fill= "green")   

def representar_consolidada(juego, ancho, alto):
    """
    Representa la superficie consolidada en la grilla
    """
    distancia_x = 450// ancho
    distancia_y = ALTO_VENTANA// alto
    for numero_fila in range(len(juego)):
        for numero_columna in range(len(juego[numero_fila])):
            if juego[numero_fila][numero_columna] == tetris.OCUPADA:
                gamelib.draw_rectangle((numero_columna*distancia_x),(numero_fila*distancia_y),(numero_columna*distancia_x)+CELDA_DE_GRILLA, (numero_fila*distancia_y)+CELDA_DE_GRILLA,outline= "black", fill= "red")

def dibujar_mini_grilla():
    """
    dibuja la mini grilla
    """
    gamelib.draw_rectangle(500,CELDA_DE_GRILLA,ANCHO_VENTANA,350,outline= "white", fill= "grey")
    for k in range(6):
        gamelib.draw_line(500+(CELDA_DE_GRILLA*k),CELDA_DE_GRILLA,500+(CELDA_DE_GRILLA*k),350, fill= "black", width = 1)
        gamelib.draw_line(500,CELDA_DE_GRILLA+(CELDA_DE_GRILLA*k),ANCHO_VENTANA,CELDA_DE_GRILLA+(CELDA_DE_GRILLA*k), fill = "black", width = 1)

def dibujar_pieza_sig(pieza_siguiente):
    """
    Representa la pieza siguiente en la ventana o mini grilla
    """
    if pieza_siguiente != None:
        for celda in pieza_siguiente:
            x,y = celda
            gamelib.draw_rectangle(500+(CELDA_DE_GRILLA*x),CELDA_DE_GRILLA+(CELDA_DE_GRILLA*y),550+(CELDA_DE_GRILLA*x),100+(CELDA_DE_GRILLA*y), outline= "black",fill = "blue")

def ver_puntos_actuales(puntos):
    """
    Presenta los puntajes actuales
    """
    gamelib.draw_text(f"Puntos: {puntos}", 500,25, size= 12, fill= "yellow", anchor= "c")

def juego_mostrar(juego, puntos, pieza_siguiente = None):
    ancho, alto = tetris.dimensiones(juego)
    crear_grilla(ancho,alto)
    pieza_actual = tetris.pieza_actual(juego)
    representar_pieza(pieza_actual, ancho, alto)
    representar_consolidada(juego, ancho, alto)
    dibujar_mini_grilla()
    dibujar_pieza_sig(pieza_siguiente)
    ver_puntos_actuales(puntos)


def juego_actualizar(juego, puntos, tecla=None, pieza_siguiente = None):
    cambio_de_pieza = None
    puntos
    dicc = TECLAS    
    if tecla in dicc and not tetris.terminado(juego):
        if dicc[tecla] == "DESCENDER":
            juego, cambio_de_pieza = tetris.avanzar(juego, pieza_siguiente)
            return (juego, cambio_de_pieza, puntos)
        elif dicc[tecla] == "GUARDAR" or dicc[tecla]== "CARGAR":
            if dicc[tecla] == "GUARDAR":
                tetris.gurdar_juego(juego,puntos)
            elif dicc[tecla]== "CARGAR":
                if tetris.cargar_partida() != None:
                    juego, puntos = tetris.cargar_partida()
        else:
            direccion = dicc[tecla]
            if direccion == "DERECHA":
                direccion = tetris.DERECHA
                juego=tetris.mover(juego, direccion)
            elif direccion == "IZQUIERDA":
                direccion = tetris.IZQUIERDA
                juego=tetris.mover(juego, direccion)
            else:
                if dicc[tecla]== "ROTAR":
                    juego = tetris.rotar(juego)


    
    return (juego, cambio_de_pieza, puntos)

def mostrar_high_score():
    """
    Encargada de mostrar las mejores puntuaciones
    """
    puntuaciones = []
    nombres = []
    contador = 0
    with open(ARCHIVO_DE_PUNTAJES) as archivo:
        for linea in archivo:
            linea = linea.rstrip("\n")
            lista = linea.split(";")
            nombres.append(lista[0])
            puntuaciones.append(lista[1])

    texto = ""
    for contador in range(len(puntuaciones)):
        texto = texto + nombres[contador]+ " " + puntuaciones[contador] + "\n"
    gamelib.say(texto)

def guardar_high_score(puntos,nombre):
    """
    Si la puntuación debe guardarse en las 10 mas altas realiza dicha tarea
    """
    if not os.path.isfile("puntajes.txt"):
        with open(ARCHIVO_DE_PUNTAJES, "w") as archivo:
            puntos = ";" + str(puntos)
            linea = nombre + puntos
            archivo.write(linea)
            archivo.write("\n")
    else:
        diccionario_de_puntos = {}
        with open(ARCHIVO_DE_PUNTAJES) as archivo:
            for linea in archivo:
                linea = linea.rstrip("\n")
                lista = linea.split(";")
                nombre_a_leer = lista[0]
                puntaje = lista[1]
                puntaje = int(puntaje)
                diccionario_de_puntos[puntaje] = nombre_a_leer
        lista_de_puntos = list(diccionario_de_puntos.keys())
        lista_de_puntos = sorted(lista_de_puntos)
        if puntos > lista_de_puntos[0] or len(lista_de_puntos) < 10:
            lista_de_puntos.append(puntos)
            diccionario_de_puntos[puntos] = nombre
            lista_de_puntos = sorted(lista_de_puntos)
        
        while len(lista_de_puntos) > 10:
            lista_de_puntos.pop(0)
        with open(ARCHIVO_DE_PUNTAJES, "w") as archivo:
            for clave in lista_de_puntos:
                    nombre_a_escribir = diccionario_de_puntos[clave]
                    linea_a_escribir = nombre_a_escribir + ";" + str(clave)
                    archivo.write(linea_a_escribir)
                    archivo.write("\n")

def verificar_top_10(puntos):
    """
    verifica si se debe dar la opción al usuario de guradar su puntuación como más alta
    """
    if not os.path.isfile(ARCHIVO_DE_PUNTAJES):
        return True
    contador = 0
    with open(ARCHIVO_DE_PUNTAJES) as archivo:
        for linea in archivo:
            contador += 1
    if contador < 10:
        return True
    else:
        puntajes_mas_altos = []
        with open (ARCHIVO_DE_PUNTAJES) as archivo:
            for linea in archivo:
                linea = linea.rstrip("\n")
                lista = linea.split(";")
                nombre_a_leer = lista[0]
                puntaje_a_leer =  lista[1]
                puntaje_a_leer = int(puntaje_a_leer)
                puntajes_mas_altos.append(puntaje_a_leer)
        puntajes_mas_altos= sorted(puntajes_mas_altos)
        if puntos > puntajes_mas_altos[0]:
            return True
        else:
            return False

gamelib.init(main)