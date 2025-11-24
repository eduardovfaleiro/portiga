from controle.controlador_admin import ControladorAdmin
from controle.controlador_capitao import ControladorCapitao
from controle.controlador_chegada import ControladorChegada
from controle.controlador_companhia import ControladorCompanhia
from controle.controlador_navio import ControladorNavio
from controle.controlador_partida import ControladorPartida
from controle.controlador_porto import ControladorPorto
from controle.controlador_relatorio import ControladorRelatorio
from telas.tela_sistema import TelaSistema
import FreeSimpleGUI as sg


class ControladorSistema:
    def __init__(self):
        self.__tela_sistema = TelaSistema()
        self.__controlador_companhia = ControladorCompanhia(self)
        self.__controlador_navio = ControladorNavio(self)
        self.__controlador_porto = ControladorPorto(self)
        self.__controlador_chegada = ControladorChegada(self)
        self.__controlador_partida = ControladorPartida(self)
        self.__controlador_capitao = ControladorCapitao(self)
        self.__controlador_relatorio = ControladorRelatorio(self)
        self.__controlador_admin = ControladorAdmin(self)

    @property
    def controlador_companhia(self):
        return self.__controlador_companhia

    @property
    def controlador_navio(self):
        return self.__controlador_navio
    
    @property
    def controlador_porto(self):
        return self.__controlador_porto

    @property
    def controlador_capitao(self):
        return self.__controlador_capitao
    
    @property
    def controlador_relatorio(self):
        return self.__controlador_relatorio
    
    @property
    def controlador_admin(self):
        return self.__controlador_admin

    def inicializa(self):
        sg.theme('Reddit')
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

    def abre_tela_capitao(self):
        self.__controlador_capitao.abre_tela()

    def abre_tela_relatorio(self):
        self.__controlador_relatorio.abre_tela()
    def abre_tela_admin(self):
        self.__controlador_admin.abre_tela()

    def encerra(self):
        exit(0)

    def abre_tela(self):
        opcoes = {1: self.abre_tela_companhia, 2: self.abre_tela_navio, 3: self.abre_tela_porto, \
                  4: self.abre_tela_chegada, 5: self.abre_tela_partida, 6: self.abre_tela_capitao, \
                    7: self.abre_tela_relatorio, 8: self.abre_tela_admin, \
                        0: self.encerra}

        while True:
            opcao_escolhida = self.__tela_sistema.abre_opcoes()
            funcao_escolhida = opcoes[opcao_escolhida]
            funcao_escolhida()

        