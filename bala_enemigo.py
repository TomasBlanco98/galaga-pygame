import pygame
from bala import Bala

class BalasEnemigos(Bala):
    def __init__(self, x, y, velocidad_bala):
        super().__init__(x, y, "img/disparo_enemigo.png", velocidad_bala)