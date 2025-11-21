from DAOs.dao import DAO
from models.companhia import Companhia

class CompanhiaDAO(DAO):
    def __init__(self):
        super().__init__('companhias.pkl')

    def add(self, companhia: Companhia):
        if((companhia is not None) and isinstance(companhia, Companhia) and isinstance(companhia.id, int)):
            super().add(companhia.id, companhia)

    def update(self, companhia: Companhia):
        if((companhia is not None) and isinstance(companhia, Companhia) and isinstance(companhia.id, int)):
            super().update(companhia.id, companhia)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)