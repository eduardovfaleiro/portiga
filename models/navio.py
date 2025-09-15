from models.pais import Pais
from models.companhia import Companhia
from models.capitao import Capitao
from models.carga import Carga

class Navio:
    def __init__(self, nome: str, bandeira: Pais, companhia: Companhia, capitao: Capitao, cargas: List[Carga]):
        self.__nome = nome
        self.__bandeira = bandeira
        self.__companhia = companhia
        self.__capitao = capitao
        self.__cargas = cargas

    @property
    def bandeira(self):
        return self.__bandeira
    
    @property
    def companhia(self):
        return self.__companhia
    
    @property
    def capitao(self):
        return self.__capitao
    
     @property
    def cargas(self):
        return self.__cargas