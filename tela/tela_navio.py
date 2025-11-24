import json
import os
import re
from typing import Any
from entidade.pais import Pais
from tela.seletor_pais import SeletorPais
from tela.tela_utils import TelaUtils
import FreeSimpleGUI as sg


class TelaNavio(TelaUtils, SeletorPais):
    def abre_opcoes(self) -> int:
        layout = [
            [sg.Text('Gerenciamento de Navios', font=('Helvetica', 20), justification='center', expand_x=True)],
            
            [sg.Button('Incluir', key=1, size=(15, 1)), sg.Button('Excluir', key=2, size=(15, 1))],
            [sg.Button('Alterar', key=3, size=(15, 1)), sg.Button('Listar', key=4, size=(15, 1))],
            
            [sg.HorizontalSeparator(pad=(0, 10))],
            
            [sg.Button('Carregar', key=5, size=(15, 1)), sg.Button('Descarregar', key=6, size=(15, 1))],
            
            [sg.Button('Retornar', key=0, button_color=('white', 'firebrick3'), pad=(0, 20))]
        ]

        window = sg.Window('Navios', layout, element_justification='c')
        event, _ = window.read()
        window.close()

        if event in (sg.WIN_CLOSED, None):
            return 0
        return int(event)

    def pega_dados_navio(self) -> dict[str, Any] | None:
        layout = [
            [sg.Text('Cadastro de Navio', font=('Helvetica', 14))],
            [sg.Text('Nome:', size=(15, 1)), sg.Input(key='nome')],
            [sg.Text('Bandeira (ISO):', size=(15, 1)), sg.Input(key='bandeira', size=(5,1)), sg.Text('(Ex: BRA, USA)')],
            [sg.Text('ID Companhia:', size=(15, 1)), sg.Input(key='companhia')],
            [sg.Text('ID Capitão:', size=(15, 1)), sg.Input(key='capitao')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Novo Navio', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None

            nome = values['nome'].strip()
            iso_bandeira = values['bandeira'].strip().upper()
            companhia_str = values['companhia'].strip()
            capitao_str = values['capitao'].strip()

            if not nome:
                sg.popup_error('Nome do navio não pode ser vazio')
                continue

            bandeira_obj = self.retorna_pais(iso_bandeira)
            if bandeira_obj is None:
                sg.popup_error('Código de país ISO 3166 não existe ou inválido.')
                continue

            if not (companhia_str.isdigit() and capitao_str.isdigit()):
                sg.popup_error('Código da Companhia e do Capitão devem ser números.')
                continue

            window.close()
            return {
                "nome": nome,
                "bandeira": bandeira_obj,
                "companhia": int(companhia_str),
                "capitao": int(capitao_str),
            }

    def pega_dados_opcionais_navio(self) -> dict[str, Any] | None:
        layout = [
            [sg.Text('Alterar Navio (Deixe vazio para manter)', font=('Helvetica', 12))],
            [sg.Text('Novo Nome:', size=(15, 1)), sg.Input(key='nome')],
            [sg.Text('Nova Bandeira:', size=(15, 1)), sg.Input(key='bandeira')],
            [sg.Text('Nova Cia ID:', size=(15, 1)), sg.Input(key='companhia')],
            [sg.Text('Novo Capitão ID:', size=(15, 1)), sg.Input(key='capitao')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Alterar Navio', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None

            nome = values['nome'].strip() or None
            iso_bandeira = values['bandeira'].strip().upper()
            companhia_str = values['companhia'].strip()
            capitao_str = values['capitao'].strip()

            bandeira_obj = None
            if iso_bandeira:
                bandeira_obj = self.retorna_pais(iso_bandeira)
                if bandeira_obj is None:
                    sg.popup_error('Código de país inválido.')
                    continue
            
            companhia_id = None
            if companhia_str:
                if not companhia_str.isdigit():
                    sg.popup_error('ID da Companhia deve ser número.')
                    continue
                companhia_id = int(companhia_str)

            capitao_id = None
            if capitao_str:
                if not capitao_str.isdigit():
                    sg.popup_error('ID do Capitão deve ser número.')
                    continue
                capitao_id = int(capitao_str)

            window.close()
            return {
                "nome": nome,
                "bandeira": bandeira_obj,
                "companhia": companhia_id,
                "capitao": capitao_id,
            }

    def pega_dados_carga(self) -> dict[str, Any] | None:
        layout = [
            [sg.Text('Dados da Carga', font=('Helvetica', 14))],
            [sg.Text('Produto:', size=(10,1)), sg.Input(key='produto')],
            [sg.Text('Tipo:', size=(10,1)), sg.Combo([1, 2, 3, 4], default_value=1, key='tipo', readonly=True)],
            [sg.Text('Peso (kg):', size=(10,1)), sg.Input(key='peso')],
            [sg.Text('Valor (R$):', size=(10,1)), sg.Input(key='valor')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Adicionar Carga', layout)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None

            produto = values['produto'].strip()
            peso_raw = values['peso'].strip()
            valor_raw = values['valor'].strip()
            tipo = values['tipo']
            
            # Validações
            if not produto:
                sg.popup_error('Produto não pode ser vazio.')
                continue

            try:
                peso = float(peso_raw)
                valor = float(valor_raw)
                if peso < 0 or valor < 0:
                    raise ValueError
            except ValueError:
                sg.popup_error('Peso e Valor devem ser números positivos.')
                continue

            window.close()
            return {'produto': produto, 'tipo': tipo, 'peso': peso, 'valor': valor} # O tipo já vem certo do Combo

    def seleciona_carga(self) -> str | None:
        return sg.popup_get_text('Digite o Código da Carga:', title='Selecionar Carga')

    def seleciona_navio(self) -> int | None:
        layout = [
            [sg.Text('Digite o ID do Navio:', font=('Helvetica', 12))],
            [sg.Input(key='id', size=(20,1))],
            [sg.Button('OK'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Selecionar Navio', layout, element_justification='c')
        
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None
            
            if values['id'].strip().isdigit():
                window.close()
                return int(values['id'])
            
            sg.popup_error('ID deve ser numérico.')

    def mostra_navio(self, navio: Any):
        if isinstance(navio, dict):
            id_ = navio.get('id', '')
            nome = navio.get('nome', '')
            bandeira = navio.get('bandeira')
            companhia = navio.get('companhia')
            capitao = navio.get('capitao')
            cargas = navio.get('cargas', [])
        else:
            id_ = getattr(navio, 'id', '')
            nome = getattr(navio, 'nome', '')
            bandeira = getattr(navio, 'bandeira', None)
            companhia = getattr(navio, 'companhia', None)
            capitao = getattr(navio, 'capitao', None)
            cargas = getattr(navio, 'cargas', [])

        bandeira_txt = f'{bandeira.codigo} {bandeira.nome}' if bandeira else 'N/A'
        companhia_txt = f'{companhia.id} {companhia.nome}' if companhia else 'N/A'
        capitao_txt = f'{capitao.id} {capitao.nome}' if capitao else 'N/A'

        cargas_str = "Nenhuma carga"
        if cargas:
            lista_cargas = []
            for c in cargas:
                cid = getattr(c, 'id', None) or getattr(c, 'codigo', None) or str(c)
                cproduto = getattr(c, 'produto', '')
                cpeso = getattr(c, 'peso', '')
                lista_cargas.append(f"[{cid}] {cproduto} ({cpeso}kg)")
            cargas_str = "\n".join(lista_cargas)

        mensagem = (
            f"ID: {id_}\n"
            f"Nome: {nome}\n"
            f"Bandeira: {bandeira_txt}\n"
            f"Companhia: {companhia_txt}\n"
            f"Capitão: {capitao_txt}\n\n"
            f"--- CARGAS ---\n{cargas_str}"
        )

        sg.popup_scrolled(mensagem, title=f'Detalhes do Navio {id_}', size=(50, 15))


    def mostra_cargas_navio(self, cargas: list):
        if not cargas:
            sg.popup('Este navio não possui cargas.', title='Vazio')
            return

        dados_tabela = []
        for c in cargas:
            cid = getattr(c, 'id', None) or getattr(c, 'codigo', '')
            cproduto = getattr(c, 'produto', '')
            ctipo = getattr(c, 'tipo', '')
            cpeso = getattr(c, 'peso', '')
            cvalor = getattr(c, 'valor', '')
            
            dados_tabela.append([cid, cproduto, ctipo, f"{cpeso} kg", f"R$ {cvalor}"])

        layout = [
            [sg.Text('Cargas Embarcadas neste Navio', font=('Helvetica', 14))],
            [sg.Text('Visualize abaixo para escolher qual ID remover', font=('Helvetica', 10))],
            [sg.Table(values=dados_tabela,
                      headings=['ID', 'Produto', 'Tipo', 'Peso', 'Valor'],
                      auto_size_columns=False,
                      col_widths=[8, 20, 5, 12, 12],
                      justification='left',
                      num_rows=min(10, len(dados_tabela)),
                      row_height=35)],
            [sg.Button('Fechar e Selecionar ID', key='OK')]
        ]

        window = sg.Window('Cargas do Navio', layout, modal=True)
        window.read()
        window.close()