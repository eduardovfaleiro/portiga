from typing import Any
from telas.movimentacao.tela_movimentacao import TelaMovimentacao

class TelaPartida(TelaMovimentacao):
    __opcoes = {1: 'Incluir', 2: 'Excluir', 3: 'Listar (resumido)', 4: 'Listar (detalhado)', 0: 'Retornar'}

    def pega_dados(self) -> dict[str, Any]:
        self.mostra_titulo('Dados Partida')
        
        navio = input("Navio: ")
        data_hora = self.pega_data_hora()
        destino = int(input('Destino (porto): '))

        return {'navio': navio, 'data_hora': data_hora, 'destino': destino}

    def abre_opcoes(self):
        self.mostra_titulo('Partida')
        self.mostra_opcoes(self.__opcoes)
        return self.recebe_opcao(self.__opcoes)