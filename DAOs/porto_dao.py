from DAOs.dao import DAO
from entidade.porto import Porto

class PortoDAO(DAO):
    def __init__(self):
        super().__init__('portos.pkl')

    def add(self, porto: Porto):
        if((porto is not None) and isinstance(porto, Porto) and isinstance(porto.id, int)):
            super().add(porto.id, porto)

    def update(self, porto: Porto):
        if((porto is not None) and isinstance(porto, Porto) and isinstance(porto.id, int)):
            super().update(porto.id, porto)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)