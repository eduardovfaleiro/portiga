

from telas.tela_utils import TelaUtils
import FreeSimpleGUI as sg

class TelaSistema(TelaUtils):
    def abre_opcoes(self) -> int:
        layout = [
            [sg.Text('Bem-vindo ao Portiga')],
            
            # Botões organizados em linhas de 2 para ficar visualmente agradável
            # O parâmetro 'key' já envia o número correto direto para o retorno
            [sg.Button('Companhias', key=1, size=(20, 1)), sg.Button('Navios', key=2, size=(20, 1))],
            [sg.Button('Portos', key=3, size=(20, 1)), sg.Button('Chegadas', key=4, size=(20, 1))],
            [sg.Button('Partidas', key=5, size=(20, 1)), sg.Button('Capitães', key=6, size=(20, 1))],
            [sg.Button('Relatórios', key=7, size=(20, 1)), sg.Button('Administradores', key=8, size=(20, 1))],
            
            [sg.HorizontalSeparator(pad=(0, 10))], # Linha divisória
            
            [sg.Button('Finalizar sistema', key=0, size=(30, 1), button_color=('white', 'firebrick'))]
        ]

        window = sg.Window('Menu Principal - Portiga', layout, element_justification='c')
        
        event, values = window.read()
        window.close()

        if event == sg.WIN_CLOSED:
            return 0
        
        # Como usamos keys numéricas (key=1, key=2...), o evento já é o int que precisamos
        return int(event)