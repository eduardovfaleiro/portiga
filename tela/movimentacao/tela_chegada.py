from typing import Any

from tela.movimentacao.tela_movimentacao import TelaMovimentacao
import FreeSimpleGUI as sg

class TelaChegada(TelaMovimentacao):
    def abre_opcoes(self) -> int:
        layout = [
            [sg.Text('Menu Chegadas', font=('Helvetica', 20), justification='center', expand_x=True)],
            [sg.Button('Incluir', key=1, size=(20, 1)), sg.Button('Excluir', key=2, size=(20, 1))],
            [sg.Button('Listar (Resumido)', key=3, size=(20, 1)), sg.Button('Listar (Detalhado)', key=4, size=(20, 1))],
            [sg.HorizontalSeparator(pad=(0, 10))],
            [sg.Button('Retornar', key=0, button_color=('white', 'firebrick3'))]
        ]

        window = sg.Window('Chegadas', layout, element_justification='c')
        event, _ = window.read()
        window.close()

        if event in (sg.WIN_CLOSED, None):
            return 0
        return int(event)

    def pega_dados(self) -> dict[str, Any] | None:
        layout = [
            [sg.Text('Dados da Chegada', font=('Helvetica', 15), pad=(0,10))],

            [sg.Text('ID do Navio:', size=(15, 1)), sg.Input(key='navio')],
            [sg.Text('Data/Hora:', size=(15, 1)), sg.Input(key='data_hora'), 
             sg.Text('(dd/mm/aa hh:mm ou vazio p/ agora)', font=('Helvetica', 8))],
            
            [sg.Text('Dias de Viagem:', size=(15, 1)), sg.Input(key='dias_viagem')],
            [sg.Text('ID Procedência:', size=(15, 1)), sg.Input(key='procedencia')],
            
            [sg.Button('Confirmar', pad=(0, 15)), sg.Button('Cancelar', pad=(0, 15))]
        ]

        window = sg.Window('Cadastrar Chegada', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None

            navio_str = values['navio']
            data_str = values['data_hora']
            dias_str = values['dias_viagem']
            procedencia_str = values['procedencia']

            if not (navio_str.isdigit() and dias_str.isdigit() and procedencia_str.isdigit()):
                sg.popup_error('Navio, Dias e Procedência devem ser números inteiros.')
                continue

            data_validada = self.valida_converte_data(data_str)
            if data_validada is None:
                sg.popup_error('Data inválida! Use o formato dd/MM/yy hh:mm')
                continue

            window.close()
            return {
                'navio': int(navio_str),
                'data_hora': data_validada,
                'dias_viagem': int(dias_str),
                'procedencia': int(procedencia_str)
            }