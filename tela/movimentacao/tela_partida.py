from typing import Any
from tela.movimentacao.tela_movimentacao import TelaMovimentacao
import FreeSimpleGUI as sg

class TelaPartida(TelaMovimentacao):
    def abre_opcoes(self) -> int:
            layout = [
                [sg.Text('Menu Partidas', font=('Helvetica', 20), justification='center', expand_x=True)],
                
                [sg.Button('Incluir', key=1, size=(20, 1)), sg.Button('Excluir', key=2, size=(20, 1))],
                [sg.Button('Listar (Resumido)', key=3, size=(20, 1)), sg.Button('Listar (Detalhado)', key=4, size=(20, 1))],
                
                [sg.HorizontalSeparator(pad=(0, 10))],
                [sg.Button('Retornar', key=0, button_color=('white', 'firebrick3'))]
            ]

            window = sg.Window('Partidas', layout, element_justification='c')
            event, _ = window.read()
            window.close()

            if event in (sg.WIN_CLOSED, None):
                return 0
            return int(event)

    def mostra_lista_resumido(self, partidas: list):
        if len(partidas) == 0:
            sg.popup('Nenhum item encontrado', title='Aviso')
            return False

        # Prepara os dados: Tabela de coluna única com o resumo de cada partida
        dados_tabela = [[partida.to_string_resumido()] for partida in partidas]

        layout = [
            [sg.Text('Partidas (Resumido)', font=('Helvetica', 15))],
            [sg.Table(values=dados_tabela,
                      headings=['Dados da Partida'], 
                      auto_size_columns=False,
                      col_widths=[60], # Largura ajustada para o texto
                      justification='left',
                      num_rows=min(20, len(dados_tabela)),
                      row_height=30)],
            [sg.Button('Fechar')]
        ]

        window = sg.Window('Listagem Resumida', layout)
        window.read()
        window.close()
        return True
    
    def mostra_lista_detalhado(self, partidas: list):
        if len(partidas) == 0:
            sg.popup('Nenhum item encontrado', title='Aviso')
            return False
        
        # Concatena todos os relatórios detalhados em uma única string
        texto_completo = ""
        for partida in partidas:
            texto_completo += partida.to_string_detalhado() + "\n"
            texto_completo += "=" * 50 + "\n" # Separador visual entre itens
        
        layout = [
            [sg.Text('Partidas (Detalhado)', font=('Helvetica', 15))],
            [sg.Multiline(default_text=texto_completo, 
                          size=(80, 20),      # Tamanho do painel de visualização
                          font=('Courier', 10), # Fonte monoespaçada para alinhamento de relatórios
                          disabled=True,
                          autoscroll=True)],
            [sg.Button('Fechar')]
        ]

        window = sg.Window('Listagem Detalhada', layout)
        window.read()
        window.close()
        return True

    def pega_dados(self) -> dict[str, Any] | None:
        layout = [
            [sg.Text('Dados da Partida', font=('Helvetica', 15), pad=(0,10))],
            
            [sg.Text('ID do Navio:', size=(15, 1)), sg.Input(key='navio')],
            
            [sg.Text('Data/Hora:', size=(15, 1)), sg.Input(key='data_hora'), 
             sg.Text('(dd/MM/yy hh:mm ou vazio p/ agora)', font=('Helvetica', 8))],
            
            [sg.Text('ID Destino:', size=(15, 1)), sg.Input(key='destino')],
            
            [sg.Button('Confirmar', pad=(0, 15)), sg.Button('Cancelar', pad=(0, 15))]
        ]

        window = sg.Window('Cadastrar Partida', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return None

            # Coleta de dados
            navio_str = values['navio'].strip()
            data_hora_str = values['data_hora'].strip()
            destino_str = values['destino'].strip()

            # --- Validação ---
            
            # 1. Valida se Navio e Destino são numéricos
            if not (navio_str.isdigit() and destino_str.isdigit()):
                sg.popup_error('ID do Navio e ID do Destino devem ser números inteiros.')
                continue

            # 2. Valida Data/Hora (usando o helper da classe pai)
            # Retorna datetime.now() se a string estiver vazia OU o objeto datetime se válido
            # Retorna None se a string for inválida
            data_hora_obj = self.valida_converte_data(data_hora_str)
            
            if data_hora_obj is None:
                sg.popup_error('Data e hora inválidos. Use dd/MM/yy hh:mm ou deixe vazio.')
                continue

            # Se tudo estiver OK
            window.close()
            return {
                'navio': int(navio_str),
                'data_hora': data_hora_obj,
                'destino': int(destino_str)
            }