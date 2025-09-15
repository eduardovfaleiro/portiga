from datetime import date
from models.navio import Navio
from models.porto import Porto

class Chegada:
    def __init__(self, navio: Navio, data: date, dias_viagem: int, procedencia: Porto):
        self.__navio = navio
        self.__data = data
        self.__dias_viagem = dias_viagem
        self.__procedencia = procedencia
        
    @property
    def navio(self):
        return self.__navio
    
    @navio.setter
    def navio(self, navio: Navio):
        if not isinstance(navio, Navio):
           raise TypeError("O navio deve ser uma instância da classe Navio.")
        self.__navio = navio
        
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, data: date):
        if not isinstance(data, date):
           raise TypeError("A data deve ser uma instância de date.")
        self.__data = data
        
    @property
    def dias_viagem(self):
        return self.__dias_viagem
    
    @dias_viagem.setter
    def dias_viagem(self, dias_viagem: int):
        if not isinstance(dias_viagem, int):
           raise TypeError("O número de dias de viagem deve ser um integer.")
        self.__dias_viagem = dias_viagem
        
    @property
    def procedencia(self):
        return self.__procedencia
    
    @procedencia.setter
    def procedencia(self, procedencia: Porto):
        if not isinstance(procedencia, Porto):
           raise TypeError("A procedencia deve ser uma instância da classe Porto.")
        self.__procedencia = procedencia