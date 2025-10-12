from models.cidade import Cidade
from models.administrador import Administrador

class Porto:
    def __init__(self, id: int, nome: str, cidade: Cidade, administrador: Administrador):
        self.__id = id
        self.__nome = nome
        self.__cidade = cidade
        self.__administrador = administrador
    
    @property
    def id(self):
        return self.__id

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

    def __str__(self):
        return (
            f'Código: {self.id}\n'
            f'Nome: {self.nome}\n'
            f'Cidade: {self.cidade}\n'
            f'Administrador: {self.administrador}'
        )
        