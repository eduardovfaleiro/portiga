from DAOs.dao import DAO
from entidade.administrador import Administrador

class AdministradorDAO(DAO):
    def __init__(self):
        super().__init__('administradores.pkl')

    def add(self, administrador: Administrador):
        if((administrador is not None) and isinstance(administrador, Administrador) and isinstance(administrador.id, int)):
            super().add(administrador.id, administrador)

    def update(self, administrador: Administrador):
        if((administrador is not None) and isinstance(administrador, Administrador) and isinstance(administrador.id, int)):
            super().update(administrador.id, administrador)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)