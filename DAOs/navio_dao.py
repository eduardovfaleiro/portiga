from DAOs.dao import DAO
from entidade.navio import Navio

class NavioDAO(DAO):
    def __init__(self):
        super().__init__('navios.pkl')

    def add(self, navio: Navio):
        if((navio is not None) and isinstance(navio, Navio) and isinstance(navio.id, int)):
            super().add(navio.id, navio)

    def update(self, navio: Navio):
        if((navio is not None) and isinstance(navio, Navio) and isinstance(navio.id, int)):
            super().update(navio.id, navio)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)