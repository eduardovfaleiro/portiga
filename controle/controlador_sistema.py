from controle.controlador_companhia import ControladorCompanhia
from telas.tela_sistema import TelaSistema


class ControladorSistema:
    def __init__(self):
        self.__tela_sistema = TelaSistema()
        self.__controlador_companhia = ControladorCompanhia(self)

    def inicializa(self):
        self.abre_tela()

    def abre_tela_companhia(self):
        self.__controlador_companhia.abre_tela()

    def encerra(self):
        exit(0)

    def abre_tela(self):
        opcoes = {1: self.abre_tela_companhia, 0: self.encerra}

        while True:
            opcao_escolhida = self.__tela_sistema.abre_opcoes()
            funcao_escolhida = opcoes[opcao_escolhida]
            funcao_escolhida()

        