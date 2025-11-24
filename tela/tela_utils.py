
import re

from utils import Utils
from valor_vazio_exception import ValorVazioException
import FreeSimpleGUI as sg

class TelaUtils(Utils):
    def mostra_erro(self, mensagem: str):
        sg.popup_error('Erro', mensagem)

    def mostra_mensagem(self, mensagem: str):
        sg.popup_ok('Sucesso', mensagem)

    def seleciona_id(self) -> int | None:
        layout = [
            [sg.Text('Digite o código que deseja selecionar:', font=('Helvetica', 12))],
            [sg.Input(key='id', size=(20, 1))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Selecionar código', layout, element_justification='c')

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None

            id_str = values['id'].strip()

            if id_str.isdigit():
                window.close()
                return int(id_str)
            
            sg.popup_error('O código deve ser um número inteiro válido.')
    
    def pega_str(self, mensagem_input: str, mensagem_erro: str) -> str:
        while True:
            try:
                string = input(mensagem_input).strip()
                if self.valor_eh_vazio(string):
                    raise ValorVazioException(mensagem_erro)
                
                return string
            except ValorVazioException as e:
                self.mostra_erro(e.args[0])

    def pega_digito(self, mensagem_input: str, mensagem_erro: str) -> int:
        while True:
            digito_str = input(mensagem_input)
            if digito_str.isdigit():
                return int(digito_str)
                
            self.mostra_erro('Código só pode ser composto por dígitos')