import pygame
from bala import BalaUsuario
from constantes import *

class Personaje:
    def __init__(self) -> None:
        self.imagen = pygame.image.load("img/x-wing.png")
        self.imagen = pygame.transform.scale(self.imagen, (60,60))
        self.rect = self.imagen.get_rect()
        self.rect.centerx = ANCHO_VENTANA / 2
        self.rect.y = ALTO_VENTANA - 70
        self.score = 0
        self.vida = 100
        self.disparo = "izquierda"
        self.contador_balas = 0

    def mover(self, direccion):
        if(direccion == "derecha"):
            incremento_x = 2
        elif(direccion == "izquierda"):
            incremento_x = -2
        nueva_posicion = self.rect.centerx + incremento_x
        if(nueva_posicion > 30 and nueva_posicion < 570):
            self.rect.centerx = self.rect.centerx + incremento_x

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def disparar(self, lista_balas):
        if self.disparo == "izquierda":
            bala = BalaUsuario(self.rect.centerx - 28, self.rect.top + 33)
            self.disparo = "derecha"
        else:
            bala = BalaUsuario(self.rect.centerx + 28, self.rect.top + 33)
            self.disparo = "izquierda"
        lista_balas.append(bala)
        self.contador_balas += 1