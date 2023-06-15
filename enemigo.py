import pygame
import random
import colores
from constantes import *
from bala_enemigo import BalasEnemigos

class Enemigo:
    def __init__(self, path, escala_x, escala_y, barra_x, barra_y) -> None:
        self.imagen = pygame.image.load(path)
        self.imagen = pygame.transform.scale(self.imagen, (escala_x, escala_y))
        self.rect = self.imagen.get_rect()
        self.rect.x = random.randrange(0, ANCHO_VENTANA - self.rect.width, 60)
        self.rect.y = random.randrange(-400, -self.rect.height, 60)
        self.velocidad = random.randrange(1, 3, 1)
        self.colisionando = False
        self.barra_largo = 30
        self.barra_x = barra_x
        self.barra_y = barra_y
    
    def actualizar(self):
        self.rect.y += self.velocidad
    
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)
    
    def disparar(self, lista_balas_enemigas):
        if self.velocidad == 1:
            velocidad_bala = 1
        elif self.velocidad == 2:
            velocidad_bala = 1.5
        bala = BalasEnemigos(self.rect.centerx, self.rect.top + 33, velocidad_bala)
        lista_balas_enemigas.append(bala)

    def verificar_colision_nave(self, nave):
        if nave.rect.colliderect(self.rect) and self.colisionando == False:
            nave.vida -= 33.4
    
    def verificar_colision_bala(self, nave, lista_balas, lista_naves_enemigas, sonido_explosion):
        balas_eliminadas = []
        for bala in lista_balas:
            if bala.rect.colliderect(self.rect):
                self.procesar_colision_bala(nave, lista_naves_enemigas, sonido_explosion)
                balas_eliminadas.append(bala)
        for bala_eliminada in balas_eliminadas:
            lista_balas.remove(bala_eliminada)

    def verificar_colision_bala_enemiga(self, nave, lista_balas_enemigas):
        balas_enemigas_eliminadas = []
        for bala_enemiga in lista_balas_enemigas:
            if bala_enemiga.rect.colliderect(nave.rect):
                nave.vida -= 33.4
                balas_enemigas_eliminadas.append(bala_enemiga)
        for bala_enemiga_eliminada in balas_enemigas_eliminadas:
            lista_balas_enemigas.remove(bala_enemiga_eliminada)
    
    def actualizar_pantalla(self, pantalla, nave, lista_balas, lista_balas_enemigas, 
                            lista_naves_enemigas, sonido_explosion)->int:
        estado = "activo"
        pygame.draw.rect(pantalla, colores.RED1, (self.rect.x + self.barra_x, self.rect.y - self.barra_y, self.barra_largo, 5))
        self.verificar_colision_bala(nave, lista_balas, lista_naves_enemigas, sonido_explosion)
        self.verificar_colision_bala_enemiga(nave, lista_balas_enemigas)
        self.verificar_colision_nave(nave)

        if self.rect.y > ALTO_VENTANA:
            self.rect.y = random.randrange(-300, -self.rect.height, 60)
            self.rect.x = random.randrange(0, ANCHO_VENTANA - self.rect.width, 60)
            self.velocidad = random.randrange(1, 3, 1)
        elif nave.vida < 0:
            sonido_explosion.play()
            estado = "perder"

        self.dibujar(pantalla)
        return nave.score, estado
    
class EnemigoUno(Enemigo):
    def __init__(self) -> None:
        super().__init__("img/enemy_uno.png", 60, 60, 15, 10)
        self.vida = 100

    def procesar_colision_bala(self, nave, lista_naves_enemigas, sonido_explosion):
        lista_naves_enemigas.remove(self)
        nave.score += 100
        sonido_explosion.play()
