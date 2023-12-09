import pygame
import random
import os
from copy import deepcopy
from graphviz import Digraph
import random
import time
import easygui


def limpiar_consola():
    if os.name == "nt":  # Para sistemas Windows
        os.system("cls")
    else:  # Para sistemas basados en Unix (Linux, macOS, etc.)
        os.system("clear")


def main(profundidad):
    # Dimensiones de la ventana
    ANCHO_VENTANA = 500
    ALTO_VENTANA = 500

    # Dimensiones de la matriz
    FILAS = 8
    COLUMNAS = 8

    # Tamaño de cada celda de la matriz
    ANCHO_CELDA = ANCHO_VENTANA // COLUMNAS
    ALTO_CELDA = ALTO_VENTANA // FILAS

    # Colores
    COLOR_FONDO = (255, 255, 255)
    COLOR_CELDA = (255, 255, 255)
    COLOR_BORDE_CELDA = (0, 0, 0)
    COLOR_PUNTUACION = (191, 202, 197)
    COLOR_RESALTAR = (152, 253, 209)

    # Rutas de las imágenes de yoshis
    RUTA_YOSHI_VERDE = "yoshi_verde.png"
    RUTA_YOSHI_ROJO = "yoshi_rojo.png"

    # Definir posiciones fijas de las monedas
    posiciones_fijas_monedas_1 = [
        [0, 0], [1, 0],
        [0, 1], [6, 0],
        [7, 0], [7, 1],
        [0, 6], [7, 6],
        [0, 7], [1, 7],
        [7, 7], [6, 7]
    ]
    
    posiciones_fijas_monedas_3 = [
        [3, 3], [4, 3],
        [3, 4], [4, 4]
    ]
    
    posiciones_yoshi = []
    while len(posiciones_yoshi) < 4:
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        nueva_posicion = [x, y]

        # Verificar que la nueva posición no esté en las posiciones fijas de las monedas
        if nueva_posicion not in posiciones_fijas_monedas_1 and nueva_posicion not in posiciones_fijas_monedas_3:
            posiciones_yoshi.append(nueva_posicion)

    # Ahora, posiciones_yoshi contiene las posiciones aleatorias de los cuatro yoshis
    print(posiciones_yoshi)

    matriz = [[0] * COLUMNAS for _ in range(FILAS)]



    puntuaciones = []

    # Agregar monedas con valor 1 en posiciones fijas
    for posicion in posiciones_fijas_monedas_1[:12]:
        puntuaciones.append({"posicion": posicion, "valor": 1, "imagen": "moneda_1_punto.png"})

    # Agregar monedas con valor 3 en posiciones fijas
    for posicion in posiciones_fijas_monedas_3[:4]:
        puntuaciones.append({"posicion": posicion, "valor": 3, "imagen": "moneda_3_puntos.png"})

    # Asignar monedas a la matriz
    for puntuacion in puntuaciones:
        x, y = puntuacion["posicion"]
        valor = puntuacion["valor"]
        matriz[y][x] = valor

    
    class Nodo:
        def __init__(
            self,
            padre,
            matriz,
            yoshi_verde_x,
            yoshi_verde_y,
            yoshi_rojo_x,
            yoshi_rojo_y,
            turno,
            profundidad,
            valorAV,
            valorAR,
            valorVR,
            valorHijos,
        ):
            self.matriz = matriz
            self.padre = padre
            self.yoshi_verde_x = yoshi_verde_x
            self.yoshi_verde_y = yoshi_verde_y
            self.yoshi_rojo_x = yoshi_rojo_x
            self.yoshi_rojo_y = yoshi_rojo_y
            self.hijosE = []
            tablero.turno = turno
            self.valorAV = valorAV
            self.valorAR = valorAR
            self.valorVR = valorVR
            self.profundidad = profundidad
            self.turno = turno
            self.hijos = self.posiciones_disponibles(self.turno)
            self.valorHijos = valorHijos

            if profundidad != 0:
                self.crear_hijos()

        def crear_hijos(self):
            if tablero.turno == -1:
                # Turno yoshi rojo
                for i in self.hijos:
                    matrizNueva = deepcopy(self.matriz)
                    valorAV = self.valorAV + self.matriz[i[0]][i[1]]
                    matrizNueva[i[0]][i[1]] = 0

                    if self.profundidad == 1:
                        nuevo_hijo = Nodo(
                            self,
                            matrizNueva,
                            i[1],
                            i[0],
                            self.yoshi_rojo_x,
                            self.yoshi_rojo_y,
                            1,
                            self.profundidad - 1,
                            valorAV,
                            self.valorAR
                            [valorAV, self.valorAR],
                            [],
                        )
                        self.hijosE.append(nuevo_hijo)
                    else:
                        nuevo_hijo = Nodo(
                            self,
                            matrizNueva,
                            i[1],
                            i[0],
                            self.yoshi_rojo_x,
                            self.yoshi_rojo_y,
                            1,
                            self.profundidad - 1,
                            valorAV,
                            self.valorAR
                            0,
                            [],
                        )
                        self.hijosE.append(nuevo_hijo)

            else:
                # Turno yoshi rojo
                for i in self.hijos:
                    matrizNueva = deepcopy(self.matriz)
                    valorAR = self.valorAR + self.matriz[i[0]][i[1]]
                    matrizNueva[i[0]][i[1]] = 0

                    if self.profundidad == 1:
                        nuevo_hijo = Nodo(
                            self,
                            matrizNueva,
                            self.yoshi_verde_x,
                            self.yoshi_verde_y,
                            i[1],
                            i[0],
                            -1,
                            self.profundidad - 1,
                            self.valorAV,
                            valorAR
                            [self.valorAV, valorAR],
                            [],
                        )
                        self.hijosE.append(nuevo_hijo)
                    else:
                        nuevo_hijo = Nodo(
                            self,
                            matrizNueva,
                            self.yoshi_verde_x,
                            self.yoshi_verde_y,
                            i[1],
                            i[0],
                            -1,
                            self.profundidad - 1,
                            self.valorAV,
                            valorAR
                            0,
                            [],
                        )
                        self.hijosE.append(nuevo_hijo)

        def evaluar(self):
            if self.valorAV > self.valorAR:
                return 1
            elif self.valorAV < self.valorAR:
                return -1
            else:
                return 0

        def raiz_nodo(nodo):
            if nodo.padre != None:
                return nodo.padre.raiz_nodo()
            else:
                return nodo

        def posiciones_disponibles(self, turno):
            posiciones = []
            for fila in range(FILAS):
                for columna in range(COLUMNAS):
                    if tablero.turno == -1:
                        if (
                            fila == self.yoshi_verde_y + 2
                            or fila == self.yoshi_verde_y - 2
                        ) and (
                            columna == self.yoshi_verde_x + 1
                            or columna == self.yoshi_verde_x - 1
                        ):
                            posiciones.append([fila, columna])

                        if (
                            fila == self.yoshi_verde_y + 1
                            or fila == self.yoshi_verde_y - 1
                        ) and (
                            columna == self.yoshi_verde_x + 2
                            or columna == self.yoshi_verde_x - 2
                        ):
                            posiciones.append([fila, columna])

                        if posiciones.__contains__(
                            [self.yoshi_rojo_y, self.yoshi_rojo_x]
                        ):
                            posiciones.remove(
                                [self.yoshi_rojo_y, self.yoshi_rojo_x]
                            )
                    else:
                        if (
                            fila == self.yoshi_rojo_y + 2
                            or fila == self.yoshi_rojo_y - 2
                        ) and (
                            columna == self.yoshi_rojo_x + 1
                            or columna == self.yoshi_rojo_x - 1
                        ):
                            posiciones.append([fila, columna])

                        if (
                            fila == self.yoshi_rojo_y + 1
                            or fila == self.yoshi_rojo_y - 1
                        ) and (
                            columna == self.yoshi_rojo_x + 2
                            or columna == self.yoshi_rojo_x - 2
                        ):
                            posiciones.append([fila, columna])

                        if posiciones.__contains__(
                            [self.yoshi_verde_y, self.yoshi_verde_x]
                        ):
                            posiciones.remove(
                                [self.yoshi_verde_y, self.yoshi_verde_x]
                            )

            if turno == 1:
                return sorted(posiciones)
            else:
                return sorted(posiciones, reverse=True)

    # Clase para representar el tablero del juego

    class Tablero:
        def __init__(self):
            # Matriz
            self.matriz = matriz
            # -1 para el yoshi verde, 1 para el yoshi rojo
            self.turno = -1
            # Atributos yoshi verde
            self.yoshi_verde_x = posiciones_yoshi[0][0]
            self.yoshi_verde_y = posiciones_yoshi[0][1]
            self.puntuacion_yoshi_verde = 0
            self.imagen_caballo_blanco = pygame.image.load(RUTA_YOSHI_VERDE)
            # Atributos yoshi rojo
            self.yoshi_rojo_x = posiciones_yoshi[1][0]
            self.yoshi_rojo_y = posiciones_yoshi[1][1]
            self.puntuacion_yoshi_rojo = 0
            self.imagen_caballo_negro = pygame.image.load(RUTA_YOSHI_ROJO)
            # Cargar imágenes
            self.imagen_1 = pygame.image.load("moneda_1_punto.png")
            self.imagen_3 = pygame.image.load("moneda_3_puntos.png")
            # Asignar imágenes a las posiciones en el tablero
            self.imagenes_en_celdas = {} 
            for puntuacion in puntuaciones:
                x, y = puntuacion["posicion"]
                valor = puntuacion["valor"]
                imagen = self.imagen_1 if valor == 1 else self.imagen_3
                self.imagenes_en_celdas[(x, y)] = {"imagen": imagen, "tomada": False}

        def tomar_puntuacion(self, x, y):
            if (x, y) in self.imagenes_en_celdas:
                imagen_celda = self.imagenes_en_celdas[(x, y)]
                if not imagen_celda["tomada"]:
                    posiciones_disponibles = self.posiciones_disponibles()
                    if [y, x] in posiciones_disponibles:
                        imagen_celda["tomada"] = True
                        print(f"Puntuación tomada en: {x}, {y}")
                        return True
            return False


        def dibujar(self, ventana, resaltar):
            ventana.fill(COLOR_FONDO)
            for fila in range(FILAS):
                for columna in range(COLUMNAS):
                    if (resaltar.__contains__([fila, columna]) and self.turno == 1):
                        pygame.draw.rect(
                            ventana,
                            COLOR_RESALTAR,
                            (
                                columna * ANCHO_CELDA,
                                fila * ALTO_CELDA,
                                ANCHO_CELDA,
                                ALTO_CELDA,
                            ),
                        )
                        pygame.draw.rect(
                            ventana,
                            COLOR_BORDE_CELDA,
                            (
                                columna * ANCHO_CELDA,
                                fila * ALTO_CELDA,
                                ANCHO_CELDA,
                                ALTO_CELDA,
                            ),
                            1,
                        )
                    elif self.matriz[fila][columna] > 0:
                        pygame.draw.rect(
                            ventana,
                            COLOR_PUNTUACION,
                            (
                                columna * ANCHO_CELDA,
                                fila * ALTO_CELDA,
                                ANCHO_CELDA,
                                ALTO_CELDA,
                            ),
                        )
                        pygame.draw.rect(
                            ventana,
                            COLOR_BORDE_CELDA,
                            (
                                columna * ANCHO_CELDA,
                                fila * ALTO_CELDA,
                                ANCHO_CELDA,
                                ALTO_CELDA,
                            ),
                            1,
                        )
                    else:
                        pygame.draw.rect(
                            ventana,
                            COLOR_CELDA,
                            (
                                columna * ANCHO_CELDA,
                                fila * ALTO_CELDA,
                                ANCHO_CELDA,
                                ALTO_CELDA,
                            ),
                        )
                        pygame.draw.rect(
                            ventana,
                            COLOR_BORDE_CELDA,
                            (
                                columna * ANCHO_CELDA,
                                fila * ALTO_CELDA,
                                ANCHO_CELDA,
                                ALTO_CELDA,
                            ),
                            1,
                        )
                        
                                           
                    if (columna, fila) in self.imagenes_en_celdas:
                        puntuacion = self.imagenes_en_celdas[(columna, fila)]
                        if not puntuacion["tomada"]:
                            imagen = puntuacion["imagen"]
                            ventana.blit(imagen, (columna * ANCHO_CELDA, fila * ALTO_CELDA))
                    
                    # Dibujar yoshi verde
                    if (
                        fila == self.yoshi_verde_y
                        and columna == self.yoshi_verde_x
                    ):
                        ventana.blit(
                            self.imagen_caballo_blanco,
                            (columna * ANCHO_CELDA, fila * ALTO_CELDA),
                        )

                    # Dibujar yoshi rojo
                    if fila == self.yoshi_rojo_y and columna == self.yoshi_rojo_x:
                        ventana.blit(
                            self.imagen_caballo_negro,
                            (columna * ANCHO_CELDA, fila * ALTO_CELDA),
                        )


        def posiciones_disponibles(self):
            posiciones = []
            for fila in range(FILAS):
                for columna in range(COLUMNAS):
                    if self.turno == -1:
                        if (
                            fila == self.yoshi_verde_y + 2
                            or fila == self.yoshi_verde_y - 2
                        ) and (
                            columna == self.yoshi_verde_x + 1
                            or columna == self.yoshi_verde_x - 1
                        ):
                            posiciones.append([fila, columna])

                        if (
                            fila == self.yoshi_verde_y + 1
                            or fila == self.yoshi_verde_y - 1
                        ) and (
                            columna == self.yoshi_verde_x + 2
                            or columna == self.yoshi_verde_x - 2
                        ):
                            posiciones.append([fila, columna])

                        if posiciones.__contains__(
                            [self.yoshi_rojo_y, self.yoshi_rojo_x]
                        ):
                            posiciones.remove(
                                [self.yoshi_rojo_y, self.yoshi_rojo_x]
                            )
                    else:
                        if (
                            fila == self.yoshi_rojo_y + 2
                            or fila == self.yoshi_rojo_y - 2
                        ) and (
                            columna == self.yoshi_rojo_x + 1
                            or columna == self.yoshi_rojo_x - 1
                        ):
                            posiciones.append([fila, columna])

                        if (
                            fila == self.yoshi_rojo_y + 1
                            or fila == self.yoshi_rojo_y - 1
                        ) and (
                            columna == self.yoshi_rojo_x + 2
                            or columna == self.yoshi_rojo_x - 2
                        ):
                            posiciones.append([fila, columna])

                        if posiciones.__contains__(
                            [self.yoshi_verde_y, self.yoshi_verde_x]
                        ):
                            posiciones.remove(
                                [self.yoshi_verde_y, self.yoshi_verde_x]
                            )

            return posiciones

        def verificarGanador(self):
            cantidadPuntuacion = 0
            for fila in range(FILAS):
                for columna in range(COLUMNAS):
                    if self.matriz[fila][columna] != 0:
                        cantidadPuntuacion += 1

            if cantidadPuntuacion == 0:
                pygame.quit()
                if self.puntuacion_yoshi_verde > self.puntuacion_yoshi_rojo:
                    easygui.msgbox(
                        msg="Has pérdido la inteligencia artificial te ha superado",
                        title="Smart Horses",
                    )
                elif self.puntuacion_yoshi_rojo > self.puntuacion_yoshi_verde:
                    easygui.msgbox(
                        msg="¡Has ganado! has superado a la inteligencia artificial",
                        title="Smart Horses",
                    )
                else:
                    easygui.msgbox(msg="¡Han quedado en empate!", title="Smart Horses")

                exit()

        def mover_caballo(self, x, y, posiciones):
            def minmax(nodo):
                valorHijos = []
                if nodo.valorVR == 0:
                    for hijo in nodo.hijosE:
                        if nodo.padre == None:
                            nodo.valorHijos.append(
                                [
                                    minmax(hijo)[0],
                                    minmax(hijo)[1],
                                    hijo.yoshi_verde_x,
                                    hijo.yoshi_verde_y,
                                ]
                            )
                        else:  
                            if nodo.padre.valorHijos == []:
                                nodo.valorHijos.append(
                                    [
                                        minmax(hijo)[0],
                                        minmax(hijo)[1],
                                        hijo.yoshi_verde_x,
                                        hijo.yoshi_verde_y,
                                    ]
                                )
                            else:  
                                meter = [
                                    minmax(hijo)[0],
                                    minmax(hijo)[1],
                                    hijo.yoshi_verde_x,
                                    hijo.yoshi_verde_y,
                                ]
                                if self.turno == 1:
                                    if meter[1] < nodo.padre.valorHijos[0][1]:
                                        nodo.valorHijos.append(
                                            [
                                                minmax(hijo)[0],
                                                minmax(hijo)[1],
                                                hijo.yoshi_verde_x,
                                                hijo.yoshi_verde_y,
                                            ]
                                        )
                                        break
                                    else: 
                                        nodo.valorHijos.append(
                                            [
                                                minmax(hijo)[0],
                                                minmax(hijo)[1],
                                                hijo.yoshi_verde_x,
                                                hijo.yoshi_verde_y,
                                            ]
                                        )
                                else:  
                                    if meter[0] > nodo.padre.valorHijos[0][0]:
                                        nodo.valorHijos.append(
                                            [
                                                minmax(hijo)[0],
                                                minmax(hijo)[1],
                                                hijo.yoshi_verde_x,
                                                hijo.yoshi_verde_y,
                                            ]
                                        )
                                        break
                                    else: 
                                        nodo.valorHijos.append(
                                            [
                                                minmax(hijo)[0],
                                                minmax(hijo)[1],
                                                hijo.yoshi_verde_x,
                                                hijo.yoshi_verde_y,
                                            ]
                                        )
                    
                    if nodo.turno == -1:
                        hijosOrdenados = sorted(
                            nodo.valorHijos, key=lambda x: x[0], reverse=True
                        )
                        lista = list(
                            filter(
                                lambda x: x[0] == hijosOrdenados[0][0], hijosOrdenados
                            )
                        )
                        randoma = random.choice(lista)
                        nodo.valorVR = randoma
                        return randoma
                    else:
                        hijos_ordenados = sorted(nodo.valorHijos, key=lambda x: x[1])
                        lista = list(
                            filter(
                                lambda x: x[1] == hijos_ordenados[0][1], hijos_ordenados
                            )
                        )
                        randoma = random.choice(lista)

                        nodo.valorVR = randoma
                        return randoma

                else:
                    return nodo.valorVR

            if posiciones.__contains__([y, x]) and self.turno == 1:
                valor = self.matriz[y][x]
                self.matriz[y][x] = 0 
                self.yoshi_rojo_x = x
                self.yoshi_rojo_y = y
                self.puntuacion_yoshi_rojo += valor
                if (x, y) in self.imagenes_en_celdas:
                    self.imagenes_en_celdas[(x, y)]["tomada"] = True
                self.turno = -1
                
                if (self.yoshi_verde_x, self.yoshi_verde_y) in self.imagenes_en_celdas:
                    puntuacion = self.imagenes_en_celdas[(self.yoshi_verde_x, self.yoshi_verde_y)]
                    if not puntuacion["tomada"]:
                        valor_puntuacion = self.matriz[self.yoshi_verde_y][self.yoshi_verde_x]
                        self.puntuacion_yoshi_verde += valor_puntuacion
                        self.matriz[self.yoshi_verde_y][self.yoshi_verde_x] = 0
                        puntuacion["tomada"] = True
                        print(f"Puntuación tomada por el yoshi verde en: {self.yoshi_verde_x}, {self.yoshi_verde_y}")
                        
            if self.turno == -1:
                raiz = Nodo(
                    None,
                    matriz,
                    self.yoshi_verde_x,
                    self.yoshi_verde_y,
                    self.yoshi_rojo_x,
                    self.yoshi_rojo_y,
                    -1,
                    profundidad,
                    0,
                    0,
                    0,
                    [],
                )
                minmax(raiz)
                
                def generar_grafo_1(nodo, grafo):
                    temp = (
                        "blanco x,y:\n"
                        + str(nodo.yoshi_verde_x)
                        + ","
                        + str(nodo.yoshi_verde_y)
                        + "\n"
                        + "negro x,y:\n"
                        + str(nodo.yoshi_rojo_x)
                        + ","
                        + str(nodo.yoshi_rojo_y)
                        + "\n"
                        + str(nodo.valorVR)
                        + "\n"
                        + str(nodo.turno)
                    )
                    grafo.node(str(id(nodo)), label=temp)
                    for hijo in nodo.hijosE:
                        grafo.edge(str(id(nodo)), str(id(hijo)))
                        generar_grafo_1(hijo, grafo)

                self.yoshi_verde_x = raiz.valorVR[2]
                self.yoshi_verde_y = raiz.valorVR[3]
                valor = self.matriz[raiz.valorVR[3]][raiz.valorVR[2]]
                self.puntuacion_yoshi_verde += valor
                self.matriz[self.yoshi_verde_y][self.yoshi_verde_x] = 0
                self.turno = 1

            # limpiar_consola()
            print("Puntuación yoshi verde: " + str(self.puntuacion_yoshi_verde))
            print("Puntuación yoshi rojo: " + str(self.puntuacion_yoshi_rojo))

            tablero.verificarGanador()
            
            if self.turno == 1:
                # Turno del jugador
                if tablero.tomar_puntuacion(x, y):
                    print("Has tomado una puntuación!")
                else:
                    print("No se ha tomado una puntuación.")

            elif self.turno == -1:
                # Turno de la IA
                raiz = Nodo(
                    None,
                    matriz,
                    self.yoshi_verde_x,
                    self.yoshi_verde_y,
                    self.yoshi_rojo_x,
                    self.yoshi_rojo_y,
                    -1,
                    profundidad,
                    0,
                    0,
                    0,
                    [],
                )
                minmax(raiz)
                self.yoshi_verde_x = raiz.valorVR[2]
                self.yoshi_verde_y = raiz.valorVR[3]
                if tablero.tomar_puntuacion(self.yoshi_verde_x, self.yoshi_verde_y):
                    print("La IA ha tomado una puntuación!")
            
    # Inicializar Pygame
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Yoshi's Battle - Click para jugar")

    # Crear el tablero
    tablero = Tablero()

    # Bucle principal del juego
    while True:
        posiciones = tablero.posiciones_disponibles()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                fila = y // ALTO_CELDA
                columna = x // ANCHO_CELDA
                tablero.mover_caballo(columna, fila, posiciones)

        tablero.dibujar(ventana, posiciones)
        pygame.display.flip()


if __name__ == "__main__":

    decision = easygui.indexbox(
        msg="Bienvenido a Yoshi's Battle, su pieza será el yoshi rojo, a continuación seleccione la dificultad, recuerde que estará relacionado con la profundidad que la IA podrá analizar para su movimiento.",
        title="Yoshi's Battle",
        choices=["Principiante", "Intermedio", "Experto"],
    )

    continuar = True

    if decision == 0:
        profundidad = 2
    elif decision == 1:
        profundidad = 4
    elif decision == 2:
        profundidad = 6
    else:
        exit()
    print(profundidad)
    main(profundidad)
