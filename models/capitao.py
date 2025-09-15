from models.pessoa import Pessoa
from models.companhia import Companhia

class Capitao(Pessoa):
    def __init__(self, nome: str, companhia: Companhia):
        super().__init__(nome)
        self.__companhia = companhia

    @property
    def companhia(self):
        return self.__companhia