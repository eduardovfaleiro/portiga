from abc import ABC, abstractmethod

class Pessoa(ABC):
    @abstractmethod
    def __init__(self, nome: str):
        self.__nome = nome

class Administrador(Pessoa):
    def __init__(self, nome: str, telefone: str):
        super().__init__(nome)
        self.__telefone = telefone

class Capitao(Pessoa):
    def __init__(self, nome: str, companhia: Companhia):
        super().__init__(nome)
        self.__telefone = telefone