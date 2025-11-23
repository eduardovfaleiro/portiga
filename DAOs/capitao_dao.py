from DAOs.dao import DAO
from entidade.capitao import Capitao

class CapitaoDAO(DAO):
    def __init__(self):
        super().__init__('capitaes.pkl')

    def add(self, capitao: Capitao):
        if((capitao is not None) and isinstance(capitao, Capitao) and isinstance(capitao.id, int)):
            super().add(capitao.id, capitao)

    def update(self, capitao: Capitao):
        if((capitao is not None) and isinstance(capitao, Capitao) and isinstance(capitao.id, int)):
            super().update(capitao.id, capitao)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)