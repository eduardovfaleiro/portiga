from entidade.pais import Pais

class Companhia:
    def __init__(self, id: int, nome: str, pais_sede: Pais):
        self.__id = id
        self.__nome = nome
        self.__pais_sede = pais_sede
        
    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if not isinstance(nome, str): # pyright: ignore[reportUnnecessaryIsInstance]
           raise TypeError("O nome da companhia deve ser uma string.")
        self.__nome = nome
        
    @property
    def pais_sede(self):
        return self.__pais_sede

    @pais_sede.setter
    def pais_sede(self, pais_sede: Pais):
        if not isinstance(pais_sede, Pais): # pyright: ignore[reportUnnecessaryIsInstance]
           raise TypeError("O nome do país sede deve ser uma instância da classe Pais.")
        self.__pais_sede = pais_sede

    def __str__(self):
        return (
            f'Código: {self.id}\n'
            f'Nome: {self.nome}\n'
            f'País sede: {self.pais_sede}'
        )