class Carga:
    def __init__(self, id: str, produto: str, tipo: int, peso: float, valor: float):
        self.__id = id
        self.__produto = produto
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
    def produto(self):
        return self.__produto

    @produto.setter
    def produto(self, produto: str):
        if not isinstance(produto, str):
            raise TypeError("O produto deve ser uma string.")
        self.__produto = produto

    @property
    def tipo(self):
        return self.__tipo
    
    @tipo.setter
    def tipo(self, tipo: int):
        if not isinstance(tipo, int):
            raise TypeError("O tipo deve ser um número inteiro.")
        if tipo < 1 or tipo > 4:
            raise ValueError("O tipo deve ser um número entre 1 e 4.")
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

    tipos_carga = {
        1: "Granel sólido",
        2: "Granel líquido",
        3: "Carga geral",
        4: "Carga conteinerizada"
    }