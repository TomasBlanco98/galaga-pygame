import pygame
import random
import colores
from constantes import *
from bala_enemigo import BalasEnemigos

class EnemigoDos:
    def __init__(self) -> None:
        self.imagen = pygame.image.load("img/enemy_dos.png")
        self.imagen = pygame.transform.scale(self.imagen, (100, 100))
        self.rect = self.imagen.get_rect()
        self.rect.x = random.randrange(0, ANCHO_VENTANA - self.rect.width, 60)
        self.rect.y = random.randrange(-400, -self.rect.height, 60)
        self.velocidad = random.randrange(1, 3, 1)
        self.visible = True
        self.vidas = 3
        self.colisionando = False
        self.barra_largo = 30
    
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

    def actualizar_pantalla(self, pantalla, nave, lista_balas, lista_balas_enemigas, lista_naves_enemigas, sonido_explosion)->int:
        estado = "activo"
        balas_eliminadas = []
        balas_enemigas_eliminadas = []
        if self.visible == True:
            if self.rect.y > ALTO_VENTANA:
                self.rect.y = random.randrange(-300, -self.rect.height)
                self.rect.x = random.randrange(0, ANCHO_VENTANA - self.rect.width)
                self.velocidad = random.randrange(1, 3, 1)
            else:
                if nave.rect.colliderect(self.rect):
                    if self.colisionando == False:
                        nave.vida -= 33.4
                        self.colisionando = True
                for e_bala in lista_balas:
                    if e_bala.rect.colliderect(self.rect):
                        self.barra_largo -= 10
                        self.vidas = self.vidas - 1
                        if self.vidas == 0:
                            sonido_explosion.play()
                            self.visible = False
                            lista_naves_enemigas.remove(self)
                            nave.score = nave.score + 150
                        balas_eliminadas.append(e_bala)
                for bala_eliminada in balas_eliminadas:
                    lista_balas.remove(bala_eliminada)

                for e_bala_enemiga in lista_balas_enemigas:
                    if e_bala_enemiga.rect.colliderect(nave.rect):
                        nave.vida -= 33.4
                        balas_enemigas_eliminadas.append(e_bala_enemiga)
                for bala_enemiga_eliminada in balas_enemigas_eliminadas:
                    lista_balas_enemigas.remove(bala_enemiga_eliminada)
                
                if(nave.vida < 0):
                    sonido_explosion.play()
                    estado = "perder"
                pygame.draw.rect(pantalla, colores.RED1, (self.rect.x + 35, self.rect.y - 12, self.barra_largo, 5))
        if self.visible == True:
            pantalla.blit(self.imagen, self.rect)
        return nave.score, estado