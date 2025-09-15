class Companhia:
    def __init__(self, nome: str, pais_sede: Pais, navios: list, capitaes: list):
        self.__nome = nome
        self.__pais_sede = pais_sede
        self.__navios = navios if navios is not None else []
        self.__capitaes = capitaes if capitaes is not None else []
        
    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome
        
    @property
    def pais_sede(self):
        return self.__pais_sede

    @pais_sede.setter
    def pais_sede(self, pais_sede: Pais):
        self.__pais_sede = pais_sede
        
    @property
    def navios(self):
        return self.__navios

    @property
    def capitaes(self):
        return self.__capitaes