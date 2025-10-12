from abc import ABC, abstractmethod

class Pessoa(ABC):
    @abstractmethod
    def __init__(self, id: int, nome: str):
        self.__id = id
        self.__nome = nome