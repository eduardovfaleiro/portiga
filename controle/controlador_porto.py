from typing import Any
from controle.gerador_id import GeradorId
from models.cidade import Cidade
from models.porto import Porto
from telas.tela_porto import TelaPorto


class ControladorPorto(GeradorId):
    def __init__(self, controlador_sistema):
        self.__portos: list[Porto] = []
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaPorto()
    
    def inclui(self):
        nome, cidade, pais = self.__tela.pega_dados()
        porto = Porto(id=self.gera_id(), nome=nome, cidade=Cidade(cidade, pais), administrador=None, partidas=[], chegadas=[],)
        self.__portos.append(porto)
        self.__tela.mostra_mensagem('Porto adicionado com sucesso!')

    def abre_tela(self):
        opcoes: dict[int, Any] = {1: self.inclui, 0: self.retorna}

        continua = True
        while continua:
            opcoes[self.__tela.abre_opcoes()]()



    def retorna(self):
        self.__controlador_sistema.abre_tela()