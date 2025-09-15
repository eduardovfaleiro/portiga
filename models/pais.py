class Pais:
    def __init__(self, nome: str):
        self.__nome = nome

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome: str):
        if not isinstance(nome, str):
            raise TypeError("O nome do país deve ser uma string.")
        self.__nome = nome