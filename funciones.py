import pygame
import colores
import random
from personaje import Personaje
from enemigo import EnemigoUno
from enemigo_dos import EnemigoDos
from constantes import *

def dibujar_vida(pantalla, x, y, vidas):
    largo = 80
    ancho = 15
    lleno = (vidas / 100) * largo
    borde = pygame.Rect(x, y, largo, ancho)
    lleno = pygame.Rect(x, y, lleno, ancho)
    pygame.draw.rect(pantalla, colores.GREEN, lleno)
    pygame.draw.rect(pantalla, colores.WHITE, borde, 2)

def crear_imagen_boton(path, ancho_boton, alto_boton):
    imagen = pygame.image.load(path)
    imagen = pygame.transform.scale(imagen, (ancho_boton, alto_boton))
    return imagen

def crear_rect_boton(imagen, pos_top, pos_left):
    rect_boton = imagen.get_rect()
    rect_boton.y = pos_top
    rect_boton.x = pos_left
    return rect_boton

def reiniciar_listas(lista_naves_enemigas, lista_balas, lista_balas_enemigas):
    lista_naves_enemigas.clear()
    lista_balas.clear()
    lista_balas_enemigas.clear()

def reiniciar_valores(acumulador_enemigos_uno, acumulador_enemigos_dos, nave, bandera):
    acumulador_enemigos_uno = CANTIDAD_ENEMIGOS_UNO
    acumulador_enemigos_dos = CANTIDAD_ENEMIGOS_DOS
    nave = Personaje()
    bandera = True
    return acumulador_enemigos_uno, acumulador_enemigos_dos, nave, bandera

def crear_lista_naves_enemigas(cantidad, tipo):
    lista = []
    for i in range(cantidad):
        if tipo == "tie":
            nave_enemiga = EnemigoUno()
        elif tipo == "destructor":
            nave_enemiga = EnemigoDos()
        lista.append(nave_enemiga)
    return lista

def crear_sonido(path, volumen):
    sonido = pygame.mixer.Sound(path)
    sonido.set_volume(volumen)
    return sonido

def mostrar_texto(escala, texto, color, pantalla, left, top):
    font = pygame.font.SysFont("Arial", escala)
    texto = font.render(texto, True, color)
    pantalla.blit(texto, (left, top))

def eventos_inicio(lista_eventos, rect_boton, rect_boton_puntos, ingreso, flag_correr, jugando):
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            flag_correr = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            lista_click = list(evento.pos)
            if(lista_click[0] > rect_boton[0] and lista_click[0] < (rect_boton[0] + rect_boton[2])):
                if(lista_click[1] > rect_boton[1] and lista_click[1] < (rect_boton[1] + rect_boton[3])):
                    jugando = 1
            if(lista_click[0] > rect_boton_puntos[0] and lista_click[0] < (rect_boton_puntos[0] + rect_boton_puntos[2])):
                if(lista_click[1] > rect_boton_puntos[1] and lista_click[1] < (rect_boton_puntos[1] + rect_boton_puntos[3])):
                    jugando = 2

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                ingreso = ingreso[0:-1]
            else:
                ingreso += evento.unicode
    return flag_correr, jugando, ingreso

def eventos_score(lista_eventos, flag_correr, rect_boton_volver, jugando):
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
                flag_correr = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            lista_click = list(evento.pos)
            if(lista_click[0] > rect_boton_volver[0] and lista_click[0] < (rect_boton_volver[0] + rect_boton_volver[2])):
                if(lista_click[1] > rect_boton_volver[1] and lista_click[1] < (rect_boton_volver[1] + rect_boton_volver[3])):
                    jugando = 0
    return flag_correr, jugando

def eventos_nivel(lista_eventos, flag_correr, timer_uno, lista_naves_enemigas, 
                  timer_segundos, lista_balas_enemigas, sonido_disparo_enemigo,
                  nave, lista_balas, sonido_disparo, segundos):
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
                segundos -= 1
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                nave.disparar(lista_balas)
                sonido_disparo.play()
    return flag_correr, segundos