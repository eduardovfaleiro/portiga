from DAOs.dao import DAO
from entidade.chegada import Chegada

class ChegadaDAO(DAO):
    def __init__(self):
        super().__init__('chegadas.pkl')

    def add(self, chegada: Chegada):
        if((chegada is not None) and isinstance(chegada, Chegada) and isinstance(chegada.id, int)):
            super().add(chegada.id, chegada)

    def update(self, chegada: Chegada):
        if((chegada is not None) and isinstance(chegada, Chegada) and isinstance(chegada.id, int)):
            super().update(chegada.id, chegada)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)