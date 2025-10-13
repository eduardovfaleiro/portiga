class Carga:
    def __init__(self, id: str, tipo: str, peso: float, valor: float):
        self.__id = id
        self.__tipo = tipo
        self.__peso = peso
        self.__valor = valor

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: str):
        if not isinstance(id, str):
            raise TypeError("O código deve ser uma string.")
        self.__id = id

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo: str):
        if not isinstance(tipo, str):
            raise TypeError("O tipo deve ser uma string.")
        self.__tipo = tipo

    @property
    def peso(self):
        return self.__peso

    @peso.setter
    def peso(self, peso: float):
        if not isinstance(peso, (float, int)):
            raise TypeError("O peso deve ser um número (float ou int).")
        if peso < 0:
            raise ValueError("O peso não pode ser negativo.")
        self.__peso = peso

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor: float):
        if not isinstance(valor, (float, int)):
            raise TypeError("O valor deve ser um número (float ou int).")
        if valor < 0:
            raise ValueError("O valor não pode ser negativo.")
        self.__valor = valor