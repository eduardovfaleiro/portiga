from models.cidade import Cidade
from models.administrador import Administrador
from models.partida import Partida
from models.chegada import Chegada

class Porto:
    def __init__(self, nome: str, cidade: Cidade, administrador: Administrador, partidas: list[Partida], chegadas: list[Chegada]):
        self.__nome = nome
        self.__cidade = cidade
        self.__administrador = administrador
        self.__partidas = list(partidas) if partidas is not None else []
        self.__chegadas = list(chegadas) if chegadas is not None else []
    
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome: str):
        if not isinstance(nome, str):
           raise TypeError("O nome do porto deve ser uma string.")
        self.__nome = nome
        
    @property
    def cidade(self):
        return self.__cidade
    
    @cidade.setter
    def cidade(self, cidade: Cidade):
        if not isinstance(cidade, Cidade):
           raise TypeError("A cidade deve ser uma instância da classe Cidade.")
        self.__cidade = cidade
        
    @property
    def administrador(self):
        return self.__administrador
    
    @administrador.setter
    def administrador(self, administrador: Administrador):
        if not isinstance(administrador, Administrador):
           raise TypeError("O administrador deve ser uma instância da classe Administrador.")
        self.__administrador = administrador
        
    @property
    def partidas(self):
        return self.__partidas.copy()

    @property
    def chegadas(self):
        return self.__chegadas.copy()