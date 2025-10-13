from typing import Any

from telas.movimentacao.tela_movimentacao import TelaMovimentacao

class TelaChegada(TelaMovimentacao):
    __opcoes = {1: 'Incluir', 2: 'Excluir', 3: 'Listar (resumido)', 4: 'Listar (detalhado)', 0: 'Retornar'}

    def pega_dados(self) -> dict[str, Any]:
        self.mostra_titulo('Dados Chegada')
        
        navio = input("Navio: ")
        data_hora = self.pega_data_hora()

        dias_viagem = int(input('Dias de viagem: '))
        procedencia = int(input('Procedência (código do porto): '))

        return {'navio': navio, 'data_hora': data_hora, 'dias_viagem': dias_viagem, \
                'procedencia': procedencia}

    def abre_opcoes(self):
        self.mostra_titulo('Chegadas')
        self.mostra_opcoes(self.__opcoes)
        return self.recebe_opcao(self.__opcoes)