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
    
    def __str__(self):
        return f'{self.codigo} {self.nome}'