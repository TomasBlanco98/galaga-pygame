import pygame
import colores
from constantes import *
from personaje import Personaje
from funciones import dibujar_vida
from funciones import crear_imagen_boton
from funciones import crear_rect_boton
from funciones import reiniciar_valores
from funciones import reiniciar_listas
from funciones import crear_lista_naves_enemigas
from funciones import crear_sonido
from funciones import mostrar_texto
from funciones import eventos_nivel
from funciones import galaxia_menu
from funciones import galaxia_scores
from base_datos import *

pygame.init()

crear_tabla_personajes_bd()

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Galaxia")

# Leer imagen fondo
imagen_galaxia = pygame.image.load("img/espacio.jpg")
imagen_galaxia = pygame.transform.scale(imagen_galaxia,(ANCHO_VENTANA, ALTO_VENTANA))

# Crear Menu
imagen_jugar = crear_imagen_boton("img/jugar.png", ANCHO_BOTON, ALTO_BOTON)
rect_boton = crear_rect_boton(imagen_jugar, POS_TOP_BOTON, POS_LEFT_BOTON)

imagen_puntaje = crear_imagen_boton("img/puntajes.png", ANCHO_BOTON_PUNTOS, ALTO_BOTON_PUNTOS)
rect_boton_puntos = crear_rect_boton(imagen_puntaje, POS_TOP_BOTON_PUNTOS, POS_LEFT_BOTON_PUNTOS)

imagen_volver = crear_imagen_boton("img/volver.png", ANCHO_BOTON_VOLVER, ALTO_BOTON_VOLVER)
rect_boton_volver = crear_rect_boton(imagen_volver, POS_TOP_BOTON_VOLVER, POS_LEFT_BOTON_VOLVER)

# Crear nave
nave = Personaje()

# Crear lista de enemigos
acumulador_enemigos_uno = CANTIDAD_ENEMIGOS_UNO
acumulador_enemigos_dos = CANTIDAD_ENEMIGOS_DOS
lista_naves_enemigas = crear_lista_naves_enemigas(acumulador_enemigos_uno, "tie")

# Crear lista de balas
lista_balas = []
# Crear lista de balas enemigas
lista_balas_enemigas = []

# Timer
timer_uno = pygame.USEREVENT + 0
pygame.time.set_timer(timer_uno, 10)

timer_segundos = pygame.USEREVENT + 1
pygame.time.set_timer(timer_segundos, 1000)

# INGRESO TEXTO DEL USUARIO
font_input = pygame.font.SysFont("Arial", 30)
ingreso = ""
ingreso_rect = pygame.Rect(220, 400, 150, 40)

# AUDIOS
pygame.mixer.init()
sonido_fondo = crear_sonido("audio/fondo.mp3", 0.1)
sonido_disparo_enemigo = crear_sonido("audio/enemigo.mp3", 0.7)
sonido_explosion = crear_sonido("audio/explosion.mp3", 0.8)
sonido_disparo = crear_sonido("audio/nave.mp3", 0.7)

sonido_fondo.play(-1)

flag_correr = True

while flag_correr:
    lista_eventos = pygame.event.get()
    pantalla.blit(imagen_galaxia, imagen_galaxia.get_rect())
    if JUGANDO == 0:
        flag_correr, ingreso, JUGANDO = galaxia_menu(pantalla, flag_correr, imagen_jugar, rect_boton, 
                                                    imagen_puntaje, rect_boton_puntos,lista_eventos, 
                                                    ingreso_rect, font_input, ingreso, JUGANDO)
    
    elif JUGANDO == 2:
        flag_correr, JUGANDO = galaxia_scores(pantalla, imagen_volver, rect_boton_volver, lista_eventos, flag_correr, JUGANDO)
        
    elif JUGANDO == 1:
        flag_correr, SEGUNDOS = eventos_nivel(lista_eventos, flag_correr, timer_uno, lista_naves_enemigas, timer_segundos, 
                                              lista_balas_enemigas,sonido_disparo_enemigo, nave, lista_balas, 
                                              sonido_disparo, SEGUNDOS)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            nave.mover("derecha")
        if keys[pygame.K_LEFT]:
            nave.mover("izquierda")
        
        nave.dibujar(pantalla)

        for bala in lista_balas:
            bala.actualizar(lista_balas)
            bala.dibujar(pantalla)

        for bala_enemiga in lista_balas_enemigas:
            bala_enemiga.actualizar(lista_balas_enemigas)
            bala_enemiga.dibujar(pantalla)

        for nave_enemiga in lista_naves_enemigas:
            score, estado = nave_enemiga.actualizar_pantalla(pantalla, nave, lista_balas, 
                                                             lista_balas_enemigas, lista_naves_enemigas, 
                                                             sonido_explosion
                                                             )
            
        if len(lista_naves_enemigas) == 0 and bandera_enemigo_dos == True:
            lista_naves_enemigas = crear_lista_naves_enemigas(acumulador_enemigos_dos, "destructor")
            bandera_enemigo_dos = False

        if len(lista_naves_enemigas) == 0 and bandera_enemigo_dos == False:
            if acumulador_enemigos_uno <= CANTIDAD_MAX_ENEMIGOS_UNO:
                acumulador_enemigos_uno += 1
            if acumulador_enemigos_dos <= CANTIDAD_MAX_ENEMIGOS_DOS:
                acumulador_enemigos_dos += 1
            bandera_enemigo_dos = True
            lista_naves_enemigas = crear_lista_naves_enemigas(acumulador_enemigos_uno, "tie")

        if estado == "perder" or SEGUNDOS == 0:
            guardar_puntaje_bd(ingreso, score)
            eliminar_personajes()
            JUGANDO = 0
            SEGUNDOS = 200
            reiniciar_listas(lista_naves_enemigas, lista_balas, lista_balas_enemigas)
            acumulador_enemigos_uno, acumulador_enemigos_dos, nave, bandera_enemigo_dos = reiniciar_valores(
                                                                                    acumulador_enemigos_uno, 
                                                                                    acumulador_enemigos_dos, 
                                                                                    nave,
                                                                                    bandera_enemigo_dos
                                                                                    )
            lista_naves_enemigas = crear_lista_naves_enemigas(acumulador_enemigos_uno, "tie")

        # Puntaje
        mostrar_texto(20, "SCORE: {0}".format(score), colores.WHITESMOKE, pantalla, 10, 10)
        # Barra de vida
        dibujar_vida(pantalla, 5, 580, nave.vida)
        # Tiempo
        mostrar_texto(20, "Tiempo: {0}".format(SEGUNDOS), colores.WHITESMOKE, pantalla, 100, 575)

    pygame.display.flip()

pygame.quit()