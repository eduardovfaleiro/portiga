from operator import attrgetter


class ControladorId:
    def __init__(self, lista_objetos_com_id: list):
        self.__lista_objetos_com_id = lista_objetos_com_id

    def gerar_id(self):
        ultimo_id = max(self.__lista_objetos_com_id, key=attrgetter('id'))
        novo_id = ultimo_id + 1
        return novo_id