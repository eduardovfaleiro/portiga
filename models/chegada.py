from datetime import Date
from models.navio import Navio
from models.porto import Porto

class Chegada:
    def __init__(self, navio: Navio, data: Date, dias_viagem: int, procedencia: Porto):
        self.__navio = navio
        self.__data = data
        self.__dias_viagem = dias_viagem
        self.__procedencia = procedencia
        
    @property
    def navio(self):
        return self.__navio
    
    @navio.setter
    def navio(self, navio: Navio):
        self.__navio = navio
        
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, data: Date):
        self.__data = data
        
    @property
    def dias_viagem(self):
        return self.__dias_viagem
    
    @dias_viagem.setter
    def dias_viagem(self, dias_viagem: int):
        self.__dias_viagem = dias_viagem
        
    @property
    def procedencia(self):
        return self.__procedencia
    
    @procedencia.setter
    def procedencia(self, procedencia: Porto):
        self.__procedencia = procedencia