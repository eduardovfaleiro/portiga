from models.pessoa import Pessoa
from models.companhia import Companhia
from models.navio import Navio

class Capitao(Pessoa):
    def __init__(self, nome: str, companhia: Companhia, navio: Navio):
        super().__init__(nome)
        self.__companhia = companhia
        self.__navio = navio

    @property
    def companhia(self):
        return self.__companhia
    
    @companhia.setter
    def companhia(self, companhia: Companhia):
        if not isinstance(companhia, Companhia):
            raise TypeError("A companhia deve ser uma instância da classe Companhia.")
        self.__companhia = companhia

    @property
    def navio(self):
        return self.__navio
    
    @navio.setter
    def navio(self, navio: Navio):
        if not isinstance(navio, Navio):
            raise TypeError("O navio deve ser uma instância da classe Navio.")
        self.__navio = navio