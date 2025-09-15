from models.pais import Pais
from models.companhia import Companhia
from models.capitao import Capitao
from models.carga import Carga

class Navio:
    def __init__(self, nome: str, bandeira: Pais, companhia: Companhia, capitao: Capitao, cargas: list[Carga]):
        self.__nome = nome
        self.__bandeira = bandeira
        self.__companhia = companhia
        self.__capitao = capitao
        self.__cargas = cargas

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome: str):
        if not isinstance(nome, str):
            raise TypeError("O nome do navio deve ser uma string.")
        self.__nome = nome

    @property
    def bandeira(self):
        return self.__bandeira
    
    @bandeira.setter
    def bandeira(self, bandeira: Pais):
        if not isinstance(bandeira, Pais):
            raise TypeError("A bandeira deve ser uma instância da classe Pais.")
        self.__bandeira = bandeira
    
    @property
    def companhia(self):
        return self.__companhia
    
    @companhia.setter
    def companhia(self, companhia: Companhia):
        if not isinstance(companhia, Companhia):
            raise TypeError("A companhia deve ser uma instância da classe Companhia.")
        self.__companhia = companhia
    
    @property
    def capitao(self):
        return self.__capitao
    
    @capitao.setter
    def capitao(self, capitao: Capitao):
        if not isinstance(capitao, Capitao):
            raise TypeError("O capitao deve ser uma instância da classe Capitao.")
        self.__capitao = capitao
    
    @property
    def cargas(self):
        return self.__cargas
    
    @cargas.setter
    def cargas(self, cargas: list[Carga]):
        if not all(isinstance(carga, Carga) for carga in cargas):
            raise TypeError("A lista de cargas deve conter apenas instâncias da classe Carga.")
        self.__cargas = cargas