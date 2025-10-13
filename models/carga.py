class Carga:
    def __init__(self, id: str, produto: str, peso: float, valor: float):
        self.__id = id
        self.__produto = produto
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
    def produto(self):
        return self.__produto

    @produto.setter
    def produto(self, produto: str):
        if not isinstance(produto, str):
            raise TypeError("O produto deve ser uma string.")
        self.__produto = produto

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