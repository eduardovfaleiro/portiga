from models.cidade import Cidade
from models.administrador import Administrador

class Porto:
    def __init__(self, nome: str, cidade: Cidade, administrador: Administrador, partidas: list, chegadas: list):
        self.__nome = nome
        self.__cidade = cidade
        self.__administrador = cidade
        self.__partidas = partidas if partidas is not None else []
        self.__chegadas = chegadas if chegadas is not None else []
    
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome
        
    @property
    def cidade(self):
        return self.__cidade
    
    @cidade.setter
    def cidade(self, cidade: Cidade):
        self.__cidade = cidade
        
    @property
    def administrador(self):
        return self.__administrador
    
    @administrador.setter
    def administrador(self, administrador: Administrador):
        self.__administrador = administrador
        
    @property
    def partidas(self):
        return self.__partidas

    @property
    def chegadas(self):
        return self.__chegadas