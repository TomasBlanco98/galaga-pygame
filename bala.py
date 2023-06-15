import pygame

class Bala:
    def __init__(self, x, y, path, velocidad):
        self.imagen = pygame.image.load(path)
        self.imagen = pygame.transform.scale(self.imagen, (10, 15))
        self.rect = self.imagen.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.velocidad = velocidad

    def actualizar(self, lista_balas):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0 or self.rect.bottom > 600:
            lista_balas.remove(self)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

class BalaUsuario(Bala):
    def __init__(self, x, y):
        super().__init__(x, y, "img/disparo.png", -2)