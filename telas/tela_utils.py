
import re

from utils import Utils
from valor_vazio_exception import ValorVazioException
import FreeSimpleGUI as sg

class TelaUtils(Utils):
    def mostra_erro(self, mensagem: str):
        sg.popup_error('Erro', mensagem)

    def mostra_titulo(self, titulo: str):
        LARGURA_TOTAL = 50
        conteudo = f" {titulo} " 
        espaco_preencher = LARGURA_TOTAL - len(conteudo)
        hifens_lado = espaco_preencher // 2
        string_hifens = "-" * hifens_lado
        
        resultado = string_hifens + conteudo + string_hifens
        
        if len(resultado) < LARGURA_TOTAL:
            resultado += "-"
            
        print(resultado)

    def mostra_opcoes(self, opcoes: dict[int, str]):
        for num_opcao, opcao in opcoes.items():
            print(f'{num_opcao} - {opcao}')

    def recebe_opcao(self, opcoes: dict[int, str],
                     mensagem_input: str = 'Escolha a opção: ',
                     erro_mensagem: str = 'Opção não existe'):
        while True:
            opcao = input(mensagem_input)

            if opcao in map(str, list(opcoes.keys())):
                return int(opcao)
            else:
                self.mostra_erro(erro_mensagem)
    
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
                
            self.mostra_erro('Código do navio só pode ser composto por dígitos')