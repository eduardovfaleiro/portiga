from abc import ABC, abstractmethod

class Pessoa(ABC):
    @abstractmethod
    def __init__(self, nome: str):
        self.__nome = nome

