import re
from typing import Any
from tela.tela_utils import TelaUtils
import FreeSimpleGUI as sg


class TelaCarga(TelaUtils):
    def __init__(self):
        sg.theme('DarkTeal9')

    def abre_opcoes(self) -> int:
        layout = [
            [sg.Text('Gerenciar Cargas', font=('Helvetica', 20), justification='center', expand_x=True)],
            
            [sg.Button('Incluir', key=1, size=(15, 1)), sg.Button('Excluir', key=2, size=(15, 1))],
            [sg.Button('Listar', key=3, size=(15, 1))],
            
            [sg.HorizontalSeparator(pad=(0, 10))],
            
            [sg.Button('Retornar', key=0, button_color=('white', 'firebrick3'), pad=(0, 20))]
        ]

        window = sg.Window('Cargas', layout, element_justification='c')
        event, _ = window.read()
        window.close()

        if event in (sg.WIN_CLOSED, None):
            return 0
        return int(event)

    def pega_dados_carga(self) -> dict[str, Any] | None:
        tipos_map = {1: '1 - Granel Sólido', 2: '2 - Granel Líquido', 3: '3 - Carga Geral', 4: '4 - Carga Conteinerizada'}
        combo_values = list(tipos_map.values())

        layout = [
            [sg.Text('Cadastro de Carga', font=('Helvetica', 14))],
            
            [sg.Text('Código (ID):', size=(12, 1)), sg.Input(key='id')],
            [sg.Text('Produto:', size=(12, 1)), sg.Input(key='produto')],
            
            [sg.Text('Tipo:', size=(12, 1)), sg.Combo(combo_values, key='tipo', readonly=True, size=(30,1))],
            
            [sg.Text('Peso (kg):', size=(12, 1)), sg.Input(key='peso')],
            [sg.Text('Valor (R$):', size=(12, 1)), sg.Input(key='valor')],
            
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Dados da Carga', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None

            id_carga = values['id'].strip()
            produto = values['produto'].strip()
            tipo_selecionado = values['tipo']
            peso_raw = values['peso'].strip()
            valor_raw = values['valor'].strip()

            if not id_carga or not produto:
                sg.popup_error('ID e Produto são obrigatórios.')
                continue
            
            if not tipo_selecionado:
                sg.popup_error('Selecione um Tipo de Carga.')
                continue
            
            tipo_int = int(tipo_selecionado.split(' - ')[0])

            try:
                peso = float(peso_raw)
                valor = float(valor_raw)
                if peso < 0 or valor < 0:
                    raise ValueError
            except ValueError:
                sg.popup_error('Peso e Valor devem ser números positivos.')
                continue

            window.close()
            return {
                'id': id_carga,
                'produto': produto,
                'tipo': tipo_int,
                'peso': peso,
                'valor': valor
            }

    def mostra_lista_cargas(self, cargas: list) -> bool:
        if not cargas:
            sg.popup('Nenhuma carga encontrada', title='Aviso')
            return False

        dados_tabela = []
        for c in cargas:
            dados_tabela.append([c.id, c.produto, c.tipo, f"{c.peso} kg", f"R$ {c.valor:.2f}"])

        layout = [
            [sg.Text('Lista de Cargas', font=('Helvetica', 15))],
            [sg.Table(values=dados_tabela,
                      headings=['ID', 'Produto', 'Tipo', 'Peso', 'Valor'],
                      auto_size_columns=False,
                      col_widths=[10, 25, 5, 12, 12],
                      justification='left',
                      num_rows=min(25, len(dados_tabela)),
                      row_height=35)],
            [sg.Button('Fechar')]
        ]

        window = sg.Window('Listagem', layout)
        window.read()
        window.close()
        return True

    def mostra_carga(self, carga: Any):
        mensagem = (
            f"Código: {getattr(carga, 'id', '')}\n"
            f"Produto: {getattr(carga, 'produto', '')}\n"
            f"Tipo: {getattr(carga, 'tipo', '')}\n"
            f"Peso: {getattr(carga, 'peso', '')} kg\n"
            f"Valor: R$ {getattr(carga, 'valor', '')}"
        )
        sg.popup(mensagem, title='Detalhe da Carga')

    def seleciona_carga(self) -> str | None:
        id_selecionado = sg.popup_get_text('Digite o Código (ID) da Carga:', title='Selecionar')
        
        if id_selecionado and id_selecionado.strip():
            if ' ' in id_selecionado.strip():
                sg.popup_error('Código inválido (não pode conter espaços).')
                return self.seleciona_carga()
            return id_selecionado.strip()
        
        return None
    
