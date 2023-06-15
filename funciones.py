import pygame
import colores
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

