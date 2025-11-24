from typing import Any
from controle.gerador_id import GeradorId
from entidade.chegada import Chegada
from tela.movimentacao.tela_chegada import TelaChegada
from DAOs.chegada_dao import ChegadaDAO
import FreeSimpleGUI as sg

class ControladorChegada(GeradorId):
    def __init__(self, controlador_sistema: Any):
        self.__chegada_DAO = ChegadaDAO()
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaChegada()

        super().__init__(self.__chegada_DAO.get_all())

    def inclui(self):
        navio, data_hora, dias_viagem, procedencia = \
            self.__tela.pega_dados().values()
        
        navio = self.__controlador_sistema.controlador_navio.pega_navio_por_id(navio)
        if navio is None:
            self.__tela.mostra_erro('Navio não encontrado')
            return
        procedencia = self.__controlador_sistema.controlador_porto.pega_porto_por_id(procedencia)

        chegada = Chegada(id=self.gera_id(), navio=navio, data_hora=data_hora, \
                          dias_viagem=dias_viagem, procedencia=procedencia)
        
        self.__chegada_DAO.add(chegada)
        self.__tela.mostra_mensagem('Chegada adicionada com sucesso!')

    def exclui(self):
        self.__tela.mostra_titulo('Excluir Chegada')

        tem_chegadas = self.lista_resumido()
        if not tem_chegadas: return

        while True:
            id = self.__tela.seleciona_id()
            if id == None: return

            chegada = self.__chegada_DAO.get(id)

            if chegada is not None:
                self.__chegada_DAO.remove(id) 
                self.__tela.mostra_mensagem(f'Chegada {chegada.id} excluída com sucesso!')
                self.lista_resumido()
                return
                    
            self.__tela.mostra_erro('Chegada não existe')

    def retorna(self):
        self.__controlador_sistema.abre_tela()

    def lista_resumido(self):
            # Verifica se tem itens
            chegadas = self.__chegada_DAO.get_all()
            if len(chegadas) == 0:
                sg.popup('Nenhum item encontrado')
                return False
            
            # Prepara os dados: Transforma cada objeto em uma lista com uma string única
            # Se to_string_resumido() retorna "ID: 1 - Navio: X", isso será uma linha da tabela
            dados_tabela = [[chegada.to_string_resumido()] for chegada in chegadas]

            layout = [
                [sg.Text('Chegadas (Resumido)', font=('Helvetica', 15))],
                [sg.Table(values=dados_tabela,
                        headings=['Dados da Chegada'], # Cabeçalho único
                        auto_size_columns=False,
                        col_widths=[60],               # Largura fixa para caber o texto
                        display_row_numbers=False,
                        justification='left',
                        num_rows=min(20, len(dados_tabela)),
                        row_height=30)],
                [sg.Button('Fechar')]
            ]

            window = sg.Window('Listagem Resumida', layout)
            window.read()
            window.close()
            return True
    
    def lista_detalhado(self):
        # Verifica se tem itens
        chegadas = self.__chegada_DAO.get_all()
        if len(chegadas) == 0:
            sg.popup('Nenhum item encontrado')
            return False
        
        # Para o detalhado, concatenamos tudo em um textão gigante
        texto_completo = ""
        for chegada in chegadas:
            texto_completo += f"{chegada.to_string_detalhado()}\n"
            texto_completo += "-" * 50 + "\n" # Adiciona uma linha separadora visual

        layout = [
            [sg.Text('Chegadas (Detalhado)', font=('Helvetica', 15))],
            # Multiline é ideal para relatórios longos ou textos com quebra de linha
            [sg.Multiline(default_text=texto_completo, 
                          size=(80, 20),    # Tamanho grande (Largura, Altura em caracteres)
                          disabled=True,    # Impede o usuário de editar o texto
                          font=('Courier', 10))], # Fonte monoespaçada alinha melhor relatórios
            [sg.Button('Fechar')]
        ]

        window = sg.Window('Listagem Detalhada', layout)
        window.read()
        window.close()
        return True

    def abre_tela(self):
        opcoes: dict[int, Any] = {1: self.inclui, 2: self.exclui, 3: self.lista_resumido, 4: self.lista_detalhado, 0: self.retorna}

        continua = True
        while continua:
            opcoes[self.__tela.abre_opcoes()]()