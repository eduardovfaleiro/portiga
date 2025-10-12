from operator import attrgetter
from typing import Any


class GeradorId:
    def __init__(self, lista_com_id: list[Any]):
        self.__lista = lista_com_id

    def gera_id(self) -> int:
        if len(self.__lista) == 0:
            return 0

        ultimo_id = max(self.__lista, key=attrgetter('id')).id
        novo_id = ultimo_id + 1
        return novo_id