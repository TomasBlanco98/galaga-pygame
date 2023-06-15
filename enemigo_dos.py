from constantes import *
from enemigo import Enemigo

class EnemigoDos(Enemigo):
    def __init__(self) -> None:
        super().__init__("img/enemy_dos.png", 100, 100, 35, 12)
        self.vidas = 3

    def procesar_colision_bala(self, nave, lista_naves_enemigas, sonido_explosion):
        self.barra_largo -= 10
        self.vidas -= 1
        if self.vidas == 0:
            lista_naves_enemigas.remove(self)
            nave.score += 150
            sonido_explosion.play()
