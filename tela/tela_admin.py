from typing import Any
from tela.tela_utils import TelaUtils
import FreeSimpleGUI as sg

class TelaAdmin(TelaUtils):
    def abre_opcoes(self) -> int:
        layout = [
            [sg.Text('Escolha a opção:')],
            [sg.Button('Incluir'), sg.Button('Excluir'), sg.Button('Listar')],
            [sg.Button('Retornar')]
        ]
        
        window = sg.Window('Administradores', layout)
        event, _ = window.read()
        window.close()

        # Mapeia o texto do botão para o ID esperado pelo controlador
        if event == 'Incluir': return 1
        if event == 'Excluir': return 2
        if event == 'Listar': return 3
        return 0  # Retornar ou fechar janela

    def pega_dados(self) -> dict:
        layout = [
            [sg.Text('Nome:'), sg.Input(key='nome')],
            [sg.Text('Telefone:'), sg.Input(key='telefone')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        
        window = sg.Window('Dados Administrador', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None

            nome = values['nome']
            telefone = values['telefone']

            # Validação direta
            if nome and telefone.isdigit():
                window.close()
                return {'nome': nome, 'telefone': int(telefone)}
            
            sg.popup('Erro: Nome vazio ou telefone inválido.')