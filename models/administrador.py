from models.pessoa import Pessoa
from models.porto import Porto

class Administrador(Pessoa):
    def __init__(self, nome: str, telefone: str, porto: Porto):
        super().__init__(nome)
        self.__telefone = telefone
        self.__porto = porto

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone: str):
        if not isinstance(telefone, str):
            raise TypeError("O telefone deve ser uma string.")
        self.__telefone = telefone
    
    @property
    def porto(self):
        return self.__porto

    @porto.setter
    def porto(self, porto: Porto):
        if not isinstance(porto, Porto):
            raise TypeError("O porto deve ser uma instância da classe Porto.")
        self.__porto = porto