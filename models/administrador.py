from models.pessoa import Pessoa


class Administrador(Pessoa):
    def __init__(self, nome: str, telefone: str):
        super().__init__(nome)
        self.__telefone = telefone

    