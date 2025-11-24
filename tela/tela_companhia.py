
from typing import Any
from entidade.companhia import Companhia
from tela.seletor_pais import SeletorPais
from tela.tela_utils import TelaUtils
import FreeSimpleGUI as sg

class TelaCompanhia(TelaUtils, SeletorPais):
    def abre_opcoes(self) -> int:
        layout = [
            [sg.Text('Gerenciar Companhias', font=('Helvetica', 20), justification='center', expand_x=True)],
            
            [sg.Button('Incluir', key=1, size=(15, 1)), sg.Button('Excluir', key=2, size=(15, 1))],
            [sg.Button('Alterar', key=3, size=(15, 1)), sg.Button('Listar', key=4, size=(15, 1))],
            
            [sg.HorizontalSeparator(pad=(0, 10))],
            
            [sg.Button('Retornar', key=0, button_color=('white', 'firebrick3'), pad=(0, 20))]
        ]

        window = sg.Window('Companhias', layout, element_justification='c')
        event, _ = window.read()
        window.close()

        if event in (sg.WIN_CLOSED, None):
            return 0
        return int(event)

    def pega_dados_companhia(self) -> dict[str, Any] | None:
        layout = [
            [sg.Text('Nova Companhia', font=('Helvetica', 14))],
            [sg.Text('Nome:', size=(15, 1)), sg.Input(key='nome')],
            [sg.Text('País Sede (ISO):', size=(15, 1)), sg.Input(key='pais'), sg.Text('(Ex: BRA, USA)')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Cadastro de Companhia', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None

            nome = values['nome'].strip()
            codigo_pais = values['pais'].strip().upper()

            if not nome:
                sg.popup_error('O Nome da companhia é obrigatório.')
                continue
            
            pais_obj = self.retorna_pais(codigo_pais)
            if pais_obj is None:
                sg.popup_error('Código de país ISO 3166 não encontrado.')
                continue

            window.close()
            return {"nome": nome, "pais_sede": pais_obj}
    
    def pega_dados_opcionais_companhia(self) -> dict[str, Any] | None:
        layout = [
            [sg.Text('Alterar Companhia (Deixe vazio para manter)', font=('Helvetica', 12))],
            [sg.Text('Novo Nome:', size=(15, 1)), sg.Input(key='nome')],
            [sg.Text('Novo País (ISO):', size=(15, 1)), sg.Input(key='pais')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Alterar Companhia', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None

            nome = values['nome'].strip()
            if not nome:
                nome = None

            codigo_pais = values['pais'].strip().upper()
            pais_obj = None

            if codigo_pais:
                pais_obj = self.retorna_pais(codigo_pais)
                if pais_obj is None:
                    sg.popup_error('Código de país ISO 3166 não encontrado.')
                    continue
            
            window.close()
            return {"nome": nome, "pais_sede": pais_obj}

    def mostra_lista_companhias(self, companhias: list):
        if not companhias:
            sg.popup('Nenhuma companhia cadastrada.', title='Aviso')
            return

        dados_tabela = []
        for comp in companhias:
            if isinstance(comp, dict):
                id_ = comp.get('id', '')
                nome = comp.get('nome', '')
                pais = comp.get('pais_sede')
            else:
                id_ = getattr(comp, 'id', '')
                nome = getattr(comp, 'nome', '')
                pais = getattr(comp, 'pais_sede', None)
            
            nome_pais = getattr(pais, 'nome', str(pais)) if pais else 'N/A'
            
            dados_tabela.append([id_, nome, nome_pais])

        layout = [
            [sg.Text('Lista de Companhias', font=('Helvetica', 15))],
            [sg.Table(values=dados_tabela,
                      headings=['ID', 'Nome', 'País Sede'],
                      auto_size_columns=False,
                      col_widths=[8, 30, 20],
                      justification='left',
                      num_rows=min(20, len(dados_tabela)),
                      row_height=35)],
            [sg.Button('Fechar')]
        ]

        window = sg.Window('Listagem', layout)
        window.read()
        window.close()

    def seleciona_companhia(self) -> int | None:
        layout = [
            [sg.Text('Informe o ID da Companhia:', font=('Helvetica', 12))],
            [sg.Input(key='id', size=(20, 1))],
            [sg.Button('OK'), sg.Button('Cancelar')]
        ]
        
        window = sg.Window('Selecionar', layout, element_justification='c')
        
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None
            
            id_str = values['id'].strip()
            if id_str.isdigit():
                window.close()
                return int(id_str)
            
            sg.popup_error('O ID deve ser numérico.')