from typing import Optional
from models.pais import Pais

class Companhia:
    def __init__(self, id: int, nome: str, pais_sede: Pais, navios: list = [], capitaes: list = []):
        self.__id = id
        self.__nome = nome
        self.__pais_sede = pais_sede
        self.__navios = navios# type: ignore
        self.__capitaes = capitaes# type: ignore
        
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
        
    @property
    def navios(self):
        return self.__navios.copy()# type: ignore

    @property
    def capitaes(self):
        return self.__capitaes.copy()# type: ignore