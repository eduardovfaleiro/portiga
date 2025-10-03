class Pais:
    def __init__(self, codigo: str, nome: str):
        self.__codigo = codigo
        self.__nome = nome

    @property
    def nome(self):
        return self.__nome
    
    @property
    def codigo(self):
        return self.__codigo
    
    @nome.setter
    def nome(self, nome: str):
        if not isinstance(nome, str): # type: ignore
            raise TypeError("O nome do país deve ser uma string.")
        self.__nome = nome

    