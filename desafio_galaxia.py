import pygame
import colores
import random
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
        pantalla.blit(imagen_jugar, rect_boton)
        pantalla.blit(imagen_puntaje, rect_boton_puntos)
        pygame.display.flip()

        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                flag_correr = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                lista_click = list(evento.pos)
                if(lista_click[0] > rect_boton[0] and lista_click[0] < (rect_boton[0] + rect_boton[2])):
                    if(lista_click[1] > rect_boton[1] and lista_click[1] < (rect_boton[1] + rect_boton[3])):
                        JUGANDO = 1
                if(lista_click[0] > rect_boton_puntos[0] and lista_click[0] < (rect_boton_puntos[0] + rect_boton_puntos[2])):
                    if(lista_click[1] > rect_boton_puntos[1] and lista_click[1] < (rect_boton_puntos[1] + rect_boton_puntos[3])):
                        JUGANDO = 2

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    ingreso = ingreso[0:-1]
                else:
                    ingreso += evento.unicode
        
        pygame.draw.rect(pantalla, colores.BLACK, ingreso_rect, 2)
        font_input_surface = font_input.render(ingreso, True, colores.BLACK)
        pantalla.blit(font_input_surface,(ingreso_rect.x+5, ingreso_rect.y+5))
    
    elif JUGANDO == 2:
        pantalla.blit(imagen_volver, rect_boton_volver)

        if evento.type == pygame.MOUSEBUTTONDOWN:
            lista_click = list(evento.pos)
            if(lista_click[0] > rect_boton_volver[0] and lista_click[0] < (rect_boton_volver[0] + rect_boton_volver[2])):
                if(lista_click[1] > rect_boton_volver[1] and lista_click[1] < (rect_boton_volver[1] + rect_boton_volver[3])):
                    JUGANDO = 0
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                flag_correr = False
        
        # Mostrar titulos
        mostrar_texto(24, "NOMBRE", colores.BLACK, pantalla, LEFT_TEXTO, TOP_TEXTO-25)
        mostrar_texto(24, "PUNTAJE", colores.BLACK, pantalla, LEFT_TEXTO*2, TOP_TEXTO-25)

        puntaje = obtener_puntajes_bd()
        # Mostrar nombres y puntajes
        for i in range(len(puntaje)):
            mostrar_texto(24, puntaje[i][1], colores.BLACK, pantalla, LEFT_TEXTO, TOP_TEXTO+(i*25))
            mostrar_texto(24, str(puntaje[i][2]), colores.BLACK, pantalla, LEFT_TEXTO*2, TOP_TEXTO+(i*25))
        
    elif JUGANDO == 1:
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                flag_correr = False
            if evento.type == pygame.USEREVENT:
                if evento.type == timer_uno:
                    for nave_enemiga in lista_naves_enemigas:
                        nave_enemiga.actualizar()
            if evento.type == pygame.USEREVENT + 1:
                if evento.type == timer_segundos:
                    for nave_enemiga in lista_naves_enemigas:
                        if (nave_enemiga.rect.y <= ALTO_VENTANA and nave_enemiga.rect.y >= 0) and random.random() < 0.7:
                            nave_enemiga.disparar(lista_balas_enemigas)
                            sonido_disparo_enemigo.play()
                    SEGUNDOS -= 1
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    nave.disparar(lista_balas)
                    sonido_disparo.play()

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

        # Puntaje
        mostrar_texto(20, "SCORE: {0}".format(score), colores.WHITESMOKE, pantalla, 10, 10)
        # Barra de vida
        dibujar_vida(pantalla, 5, 580, nave.vida)
        # Tiempo
        mostrar_texto(20, "Tiempo: {0}".format(SEGUNDOS), colores.WHITESMOKE, pantalla, 100, 575)

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
    pygame.display.flip()

pygame.quit()