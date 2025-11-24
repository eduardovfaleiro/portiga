from typing import Any
from tela.seletor_pais import SeletorPais
from tela.tela_utils import TelaUtils

import FreeSimpleGUI as sg

class TelaPorto(TelaUtils, SeletorPais):
    def mostra_lista_portos(self, portos: list):
        if not portos:
            sg.popup('Nenhum porto encontrado.', title='Aviso')
            return

        dados_tabela = []
        for porto in portos:
            # 1. Extração de dados (compatível com dict/objeto)
            if isinstance(porto, dict):
                id_ = porto.get('id', '')
                nome = porto.get('nome', '')
                cidade = porto.get('cidade')
                admin = porto.get('administrador')
            else:
                id_ = getattr(porto, 'id', '')
                nome = getattr(porto, 'nome', '')
                cidade = getattr(porto, 'cidade', None)
                admin = getattr(porto, 'administrador', None)

            # 2. Extração dos dados aninhados (CIDADE E PAÍS)
            
            # Assume que "cidade" pode ser um objeto Cidade, um dicionário, ou uma string
            nome_cidade = getattr(cidade, 'nome', str(cidade)) if cidade else 'N/A'
            
            # Tenta extrair o objeto PAIS de dentro do objeto/dicionário CIDADE
            if isinstance(cidade, dict):
                pais = cidade.get('pais')
            elif cidade is not None:
                pais = getattr(cidade, 'pais', None)
            else:
                pais = None
                
            # 3. Formatação dos dados aninhados
            nome_pais = getattr(pais, 'nome', str(pais)) if pais else 'N/A'
            
            # Administrador: se for um objeto, tenta obter ID e Nome.
            admin_info = f"{getattr(admin, 'nome', str(admin))}" if admin else 'N/A'
            
            # 4. Adiciona a linha na tabela
            dados_tabela.append([id_, nome, nome_cidade, nome_pais, admin_info])

        # 5. Construção do Layout da Janela
        layout = [
            [sg.Text('Lista de Portos', font=('Helvetica', 15))],
            [sg.Table(values=dados_tabela,
                    headings=['ID', 'Nome', 'Cidade', 'País', 'Administrador'],
                    auto_size_columns=False,
                    col_widths=[6, 18, 18, 15, 18],
                    justification='left',
                    num_rows=min(20, len(dados_tabela)),
                    row_height=35)],
            [sg.Button('Fechar')]
        ]

        window = sg.Window('Listagem de Portos', layout)
        window.read()
        window.close()

    def pega_dados(self) -> dict[str, Any] | None:
        layout = [
            [sg.Text('Cadastro de Porto', font=('Helvetica', 14))],
            # Campos obrigatórios
            [sg.Text('Nome:', size=(15, 1)), sg.Input(key='nome')],
            [sg.Text('Cidade:', size=(15, 1)), sg.Input(key='cidade')],
            
            # Validação com método herdado
            [sg.Text('País (código ISO):', size=(15, 1)), sg.Input(key='pais', size=(5,1))],
            
            # Novo campo
            [sg.Text('ID Administrador:', size=(15, 1)), sg.Input(key='administrador')],
            
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Novo Porto', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None

            # Coleta e limpeza dos dados
            nome = values['nome'].strip()
            cidade = values['cidade'].strip()
            iso_pais = values['pais'].strip().upper()
            id_admin_raw = values['administrador'].strip()

            # --- Validações Consolidadas ---
            if not nome:
                sg.popup_error('O Nome do porto é obrigatório.')
                continue
            
            if not cidade:
                sg.popup_error('A Cidade é obrigatória.')
                continue

            if not id_admin_raw.isdigit():
                sg.popup_error('ID do Administrador deve ser um número inteiro.')
                continue

            # Validação do País (Método herdado de SeletorPais)
            pais_obj = self.retorna_pais(iso_pais)
            if pais_obj is None:
                sg.popup_error('Código de país ISO 3166 não encontrado.')
                continue

            # Sucesso
            window.close()
            return {
                'nome': nome, 
                'cidade': cidade, 
                'pais': pais_obj, 
                'administrador': int(id_admin_raw)
            }

    def pega_dados_opcionais(self) -> dict[str, Any] | None:
        layout = [
            [sg.Text('Alterar Porto (Deixe vazio para manter)', font=('Helvetica', 14))],
            
            [sg.Text('Novo Nome:', size=(20, 1)), sg.Input(key='nome')],
            [sg.Text('Nova Cidade:', size=(20, 1)), sg.Input(key='cidade')],
            
            [sg.Text('Novo País (código ISO):', size=(20, 1)), sg.Input(key='pais', size=(5,1))],
            [sg.Text('Novo ID Administrador:', size=(20, 1)), sg.Input(key='administrador')],
            
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Novos Dados Porto', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None

            # 1. Coleta e Normalização: Converte string vazia ("") para None
            nome = values['nome'].strip() or None
            cidade = values['cidade'].strip() or None
            iso_pais = values['pais'].strip().upper()
            id_admin_raw = values['administrador'].strip()

            pais_obj = None
            id_admin = None

            # 2. Validação Condicional do País
            if iso_pais:
                pais_obj = self.retorna_pais(iso_pais)
                if pais_obj is None:
                    sg.popup_error('Código de país ISO 3166 não existe.')
                    continue # Mantém a janela aberta

            # 3. Validação Condicional do ID Administrador
            if id_admin_raw:
                if not id_admin_raw.isdigit():
                    sg.popup_error('ID do Administrador deve ser um número inteiro.')
                    continue # Mantém a janela aberta
                id_admin = int(id_admin_raw) # Converte para int

            # 4. Sucesso
            window.close()
            return {
                "nome": nome,
                "cidade": cidade,
                "pais": pais_obj,        # Objeto Pais ou None
                "administrador": id_admin, # int ou None
            }
        
    def abre_opcoes(self) -> int:
        layout = [
            [sg.Text('Gerenciar Portos', font=('Helvetica', 20), justification='center', expand_x=True)],
            
            # Botões mapeados para as chaves do dicionário
            [sg.Button('Incluir', key=1, size=(15, 1)), sg.Button('Excluir', key=2, size=(15, 1))],
            [sg.Button('Alterar', key=3, size=(15, 1)), sg.Button('Listar', key=4, size=(15, 1))],
            
            [sg.HorizontalSeparator(pad=(0, 10))],
            
            [sg.Button('Retornar', key=0, button_color=('white', 'firebrick3'), pad=(0, 20))]
        ]

        # Cria a janela e centraliza os elementos
        window = sg.Window('Menu Portos', layout, element_justification='c')
        event, _ = window.read()
        window.close()

        # O FreeSimpleGUI retorna a 'key' do botão clicado (que é o int esperado)
        if event in (sg.WIN_CLOSED, None):
            return 0
        return int(event)