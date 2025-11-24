from typing import Any
from controle.gerador_id import GeradorId
from entidade.partida import Partida
from tela.movimentacao.tela_partida import TelaPartida
from DAOs.partida_dao import PartidaDAO


class ControladorPartida(GeradorId):
    def __init__(self, controlador_sistema: Any):
        self.__partida_DAO = PartidaDAO()
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaPartida()
        super().__init__(self.__partida_DAO.get_all())

    def inclui(self):
        dados = self.__tela.pega_dados()
        if dados is None: return

        navio, data_hora, destino = dados.values()
        
        navio = self.__controlador_sistema.controlador_navio.pega_navio_por_id(navio)
        if navio is None:
            self.__tela.mostra_erro('Navio não encontrado')
            return
        destino = self.__controlador_sistema.controlador_porto.pega_porto_por_id(destino)

        partida = Partida(self.gera_id(), navio, data_hora, destino)
        
        self.__partida_DAO.add(partida)
        self.__tela.mostra_mensagem('Partida adicionada com sucesso!')

    def exclui(self):
        tem_partidas = self.lista_resumido()
        if not tem_partidas: return

        while True:
            id = self.__tela.seleciona_id()
            if id == None: return

            partida = self.__partida_DAO.get(id)

            if partida is not None:
                self.__partida_DAO.remove(id)
                self.__tela.mostra_mensagem(f'Partida {partida.id} excluída com sucesso!')
                self.lista_resumido()
                return
                    
            self.__tela.mostra_erro('Partida não existe')

    def retorna(self):
        self.__controlador_sistema.abre_tela()

    def lista_resumido(self):
        partidas = self.__partida_DAO.get_all()
        self.__tela.mostra_lista_resumido(partidas)
        
        return True

    def lista_detalhado(self):
        partidas = self.__partida_DAO.get_all()
        self.__tela.mostra_lista_detalhado(partidas)
        
        return True

    def abre_tela(self):
        opcoes: dict[int, Any] = {1: self.inclui, 2: self.exclui, 3: self.lista_resumido, 4: self.lista_detalhado, 0: self.retorna}

        continua = True
        while continua:
            opcoes[self.__tela.abre_opcoes()]()