from models.pessoa import Pessoa

class Administrador(Pessoa):
    def __init__(self, nome: str, telefone: str):
        super().__init__(nome)
        self.__telefone = telefone

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone: str):
        if not isinstance(telefone, str):
            raise TypeError("O telefone deve ser uma string.")
        self.__telefone = telefone