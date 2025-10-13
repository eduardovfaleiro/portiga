from models.pessoa import Pessoa

class Capitao(Pessoa):
    def __init__(self, id: int, nome: str):
        super().__init__(id, nome)
        self.__id = id
        self.__nome = nome
