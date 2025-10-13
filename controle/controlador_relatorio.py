from typing import Any
from models.relatorio import Relatorio
from telas.tela_relatorio import TelaRelatorio

class ControladorRelatorio:
    def __init__(self, controlador_sistema: Any):
        self.__relatorio = Relatorio()
        self.__tela = TelaRelatorio()
        self.__controlador_sistema = controlador_sistema

    def registra_carregamento(self, carga):
        self.__relatorio.registra_carregamento(carga)

    def registra_descarregamento(self, carga):
        self.__relatorio.registra_descarregamento(carga)

    def mostra_relatorio(self):
        estatisticas = self.__relatorio.get_estatisticas()
        self.__tela.mostra_relatorio(estatisticas)

    def abre_tela(self):
        self.mostra_relatorio()
