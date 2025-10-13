from typing import Any
from controle.gerador_id import GeradorId
from models.partida import Partida
from telas.movimentacao.tela_partida import TelaPartida


class ControladorPartida(GeradorId):
    def __init__(self, controlador_sistema: Any):
        self.__partidas: list[Partida] = []
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaPartida()

        super().__init__(self.__partidas)

    def inclui(self):
        navio, data_hora, destino = self.__tela.pega_dados().values()
        partida = Partida(self.gera_id(), navio, data_hora, destino)
        
        self.__partidas.append(partida)
        self.__tela.mostra_mensagem('Partida adicionada com sucesso!')

    def exclui(self):
        self.__tela.mostra_titulo('Excluir Partida')

        tem_partidas = self.lista_resumido()
        if not tem_partidas: return

        while True:
            id = self.__tela.seleciona_id()
            if id == None: return

            for i in range(len(self.__partidas)):
                partida = self.__partidas[i]
                if partida.id == id:
                    self.__partidas.pop(i)
                    self.__tela.mostra_mensagem(f'Partida {partida.id} excluída com sucesso!')
                    self.lista_resumido()
                    return
                    
            self.__tela.mostra_erro('Chegada não existe')

    def retorna(self):
        self.__controlador_sistema.abre_tela()

    def lista_resumido(self):
        print('\nListando partidas (resumido)...')

        if len(self.__partidas) == 0:
            print('Nenhum item encontrado')
            return False
        
        for partida in self.__partidas:
            print(f'{partida.to_string_resumido()}')
        
        # Adiciona line break no fim. Não remover.
        print()

        return True
    
    def lista_detalhado(self):
        print('\nListando partidas (detalhado)...')

        if len(self.__partidas) == 0:
            print('Nenhum item encontrado')
            return False
        
        for partida in self.__partidas:
            print(f'{partida.to_string_detalhado()}\n')
        
        return True

    def abre_tela(self):
        opcoes: dict[int, Any] = {1: self.inclui, 2: self.exclui, 3: self.lista_resumido, 4: self.lista_detalhado, 0: self.retorna}

        continua = True
        while continua:
            opcoes[self.__tela.abre_opcoes()]()