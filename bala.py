import pygame
import colores

class Balas:
    def __init__(self, x, y):
        self.imagen = pygame.image.load("img/disparo.png")
        self.imagen = pygame.transform.scale(self.imagen, (10,15))
        self.rect = self.imagen.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.velocidad = -2
    
    def actualizar(self, lista_balas):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0:
            lista_balas.remove(self)
    
    def dibujar(self, pantalla):
        # pygame.draw.rect(pantalla, colores.BLUE, self.rect)
        pantalla.blit(self.imagen, self.rect)