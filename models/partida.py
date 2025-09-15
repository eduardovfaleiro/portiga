from models.navio import Navio
from models.porto import Porto

class Partida:
    def __init__(self, navio: Navio, data: datetime, destino: Porto):
        self.__navio = navio
        self.__data = data
        self.__destino = destino

    @property
    def navio(self):
        return self.__navio
    
    @property
    def data(self):
        return self.__data
    
    @property
    def destino(self):
        return self.__destino