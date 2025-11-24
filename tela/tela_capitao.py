import re
from typing import Any
from entidade.capitao import Capitao
from tela.tela_utils import TelaUtils
import FreeSimpleGUI as sg

class TelaCapitao(TelaUtils):
    def abre_opcoes(self) -> int:
        layout = [
            [sg.Text('Gerenciar Capitães', font=('Helvetica', 20), justification='center', expand_x=True)],
            [sg.Button('Incluir', key=1, size=(15, 1)), sg.Button('Excluir', key=2, size=(15, 1)), sg.Button('Listar', key=3, size=(15, 1))],
            [sg.Button('Retornar', key=0, button_color=('white', 'firebrick3'), pad=(0, 20))]
        ]

        window = sg.Window('Capitães', layout, element_justification='c')
        event, _ = window.read()
        window.close()

        if event in (sg.WIN_CLOSED, None):
            return 0
        
        return int(event)

    def pega_dados_capitao(self) -> dict[str, Any] | None:
        layout = [
            [sg.Text('Nome do Capitão:', size=(15, 1)), sg.Input(key='nome')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Dados do Capitão', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None

            nome = values['nome'].strip()

            if nome:
                window.close()
                return {'nome': nome}
            
            sg.popup_error('O nome não pode ser vazio.')

    def seleciona_capitao(self) -> int | None:
        layout = [
            [sg.Text('Digite o Código (ID) do Capitão:', font=('Helvetica', 12))],
            [sg.Input(key='id', size=(20, 1))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Selecionar Capitão', layout, element_justification='c')

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None

            user_input = values['id'].strip()

            if user_input.isdigit():
                window.close()
                return int(user_input)
            
            sg.popup_error('Código inválido. Informe apenas dígitos.')

    def mostra_capitao(self, capitao: Capitao):
        mensagem = f"Código: {capitao.id}\nNome: {capitao.nome}"
        sg.popup('Detalhes do Capitão', mensagem, font=('Helvetica', 12))

    def mostra_erro(self, mensagem: str):
        sg.popup_error('Erro', mensagem)