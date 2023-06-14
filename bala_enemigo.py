import pygame
import colores

class BalasEnemigos:
    def __init__(self, x, y, velocidad_bala):
        self.imagen = pygame.image.load("img/disparo_enemigo.png")
        self.imagen = pygame.transform.scale(self.imagen, (10,15))
        self.rect = self.imagen.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.velocidad = velocidad_bala
    
    def actualizar(self, lista_balas):
        self.rect.y += self.velocidad
        if self.rect.bottom > 600:
            lista_balas.remove(self)
    
    def dibujar(self, pantalla):
        # pygame.draw.rect(pantalla, colores.BLUE, self.rect)
        pantalla.blit(self.imagen, self.rect)