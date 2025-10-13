from controle.controlador_chegada import ControladorChegada
from controle.controlador_companhia import ControladorCompanhia
from controle.controlador_navio import ControladorNavio
from controle.controlador_partida import ControladorPartida
from controle.controlador_porto import ControladorPorto
from telas.tela_sistema import TelaSistema


class ControladorSistema:
    def __init__(self):
        self.__tela_sistema = TelaSistema()
        self.__controlador_companhia = ControladorCompanhia(self)
        self.__controlador_navio = ControladorNavio(self)
        self.__controlador_porto = ControladorPorto(self)
        self.__controlador_chegada = ControladorChegada(self)
        self.__controlador_partida = ControladorPartida(self)

    def inicializa(self):
        self.abre_tela()

    def abre_tela_companhia(self):
        self.__controlador_companhia.abre_tela()

    def abre_tela_navio(self):
        self.__controlador_navio.abre_tela()

    def abre_tela_porto(self):
        self.__controlador_porto.abre_tela()

    def abre_tela_chegada(self):
        self.__controlador_chegada.abre_tela()

    def abre_tela_partida(self):
        self.__controlador_partida.abre_tela()

    def encerra(self):
        exit(0)

    def abre_tela(self):
        opcoes = {1: self.abre_tela_companhia, 2: self.abre_tela_navio, 3: self.abre_tela_porto, 4: self.abre_tela_chegada, 5: self.abre_tela_partida, 0: self.encerra}

        while True:
            opcao_escolhida = self.__tela_sistema.abre_opcoes()
            funcao_escolhida = opcoes[opcao_escolhida]
            funcao_escolhida()

        