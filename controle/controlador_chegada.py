from typing import Any
from controle.gerador_id import GeradorId
from models.chegada import Chegada
from telas.movimentacao.tela_chegada import TelaChegada

class ControladorChegada(GeradorId):
    def __init__(self, controlador_sistema: Any):
        self.__chegadas: list[Chegada] = []
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaChegada()

        super().__init__(self.__chegadas)

    def inclui(self):
        navio, data_hora, dias_viagem, procedencia = \
            self.__tela.pega_dados().values()
        chegada = Chegada(id=self.gera_id(), navio=None, data_hora=data_hora, \
                          dias_viagem=dias_viagem, procedencia=procedencia)
        
        self.__chegadas.append(chegada)
        self.__tela.mostra_mensagem('Chegada adicionada com sucesso!')

    def exclui(self):
        self.__tela.mostra_titulo('Excluir Chegada')

        tem_chegadas = self.lista_resumido()
        if not tem_chegadas: return

        while True:
            id = self.__tela.seleciona_id()
            if id == None: return

            for i in range(len(self.__chegadas)):
                chegada = self.__chegadas[i]
                if chegada.id == id:
                    self.__chegadas.pop(i)
                    self.__tela.mostra_mensagem(f'Chegada {chegada.id} excluída com sucesso!')
                    self.lista_resumido()
                    return
                    
            self.__tela.mostra_erro('Chegada não existe')

    def retorna(self):
        self.__controlador_sistema.abre_tela()

    def lista_resumido(self):
        print('\nListando chegadas (resumido)...')

        if len(self.__chegadas) == 0:
            print('Nenhum item encontrado')
            return False
        
        for chegada in self.__chegadas:
            print(f'{chegada.to_string_resumido()}')
        
        # Adiciona line break no fim. Não remover.
        print()

        return True
    
    def lista_detalhado(self):
        print('\nListando chegadas (detalhado)...')

        if len(self.__chegadas) == 0:
            print('Nenhum item encontrado')
            return False
        
        for chegada in self.__chegadas:
            print(f'{chegada.to_string_detalhado()}\n')
        
        return True

    def abre_tela(self):
        opcoes: dict[int, Any] = {1: self.inclui, 2: self.exclui, 3: self.lista_resumido, 4: self.lista_detalhado, 0: self.retorna}

        continua = True
        while continua:
            opcoes[self.__tela.abre_opcoes()]()