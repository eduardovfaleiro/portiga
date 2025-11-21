from DAOs.dao import DAO
from models.carga import Carga

class CargaDAO(DAO):
    def __init__(self):
        super().__init__('cargas.pkl')

    def add(self, carga: Carga):
        if((carga is not None) and isinstance(carga, Carga) and isinstance(carga.id, int)):
            super().add(carga.id, carga)

    def update(self, carga: Carga):
        if((carga is not None) and isinstance(carga, Carga) and isinstance(carga.id, int)):
            super().update(carga.id, carga)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)