from datetime import date
from models.navio import Navio
from models.porto import Porto

class Partida:
    def __init__(self, navio: Navio, data: date, destino: Porto):
        self.__navio = navio
        self.__data = data
        self.__destino = destino

    @property
    def navio(self):
        return self.__navio
    
    @navio.setter
    def navio(self, navio: Navio):
        if not isinstance(navio, Navio):
            raise TypeError("O valor do navio deve ser uma instância da classe Navio.")
        self.__navio = navio
    
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, data: date):
        if not isinstance(data, date):
            raise TypeError("O valor da data deve ser uma instância da classe date.")
        self.__data = data
    
    @property
    def destino(self):
        return self.__destino

    @destino.setter
    def destino(self, destino: Porto):
        if not isinstance(destino, Porto):
            raise TypeError("O valor do destino deve ser uma instância da classe Porto.")
        self.__destino = destino