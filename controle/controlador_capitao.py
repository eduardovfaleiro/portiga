from operator import attrgetter
from typing import Any
from controle.gerador_id import GeradorId
from entidade.capitao import Capitao
from tela.tela_capitao import TelaCapitao
from DAOs.capitao_dao import CapitaoDAO
import FreeSimpleGUI as sg

class ControladorCapitao(GeradorId):
    def __init__(self, controlador_sistema):  # type: ignore
        self.__capitao_DAO = CapitaoDAO()
        self.__controlador_sistema = controlador_sistema
        self.__tela_capitao = TelaCapitao()
        super().__init__(self.__capitao_DAO.get_all())

    def inclui(self):
        dados = self.__tela_capitao.pega_dados_capitao()
        if not dados:
            return
        capitao = Capitao(self.gera_id(), dados['nome'])
        self.__capitao_DAO.add(capitao)
        self.__tela_capitao.mostra_mensagem('Capitão adicionado com sucesso!')

    def pega_capitao_por_id(self, id: int):
        return self.__capitao_DAO.get(id)

    def exclui(self):
        self.__tela_capitao.mostra_titulo('Excluir Capitão')

        if not self.lista():
            return

        selecionado = self.__tela_capitao.seleciona_capitao()  # espera ID
        if selecionado is None:
            return

        capitao = self.__capitao_DAO.get(selecionado)

        if capitao is None:
            self.__tela_capitao.mostra_erro('Capitão não encontrado')
            return

        self.__capitao_DAO.remove(selecionado)
        self.__tela_capitao.mostra_mensagem(f'Capitão {capitao.nome} (ID: {capitao.id}) removido com sucesso!')
        self.lista()

    def lista(self) -> bool:
        capitaes = self.__capitao_DAO.get_all()

        if len(capitaes) == 0:
            sg.popup('Nenhum capitão encontrado')
            return False

        # 1. Prepara os dados para a tabela (Matriz de strings/números)
        dados_tabela = []
        for capitao in capitaes:
            # Adicione aqui os atributos que deseja mostrar (ex: ID e Nome)
            dados_tabela.append([capitao.id, capitao.nome])

        # 2. Define o Layout
        layout = [
            [sg.Text('Lista de Capitães', font=('Helvetica', 15))],
            [sg.Table(values=dados_tabela,
                      headings=['Código', 'Nome'],      # Títulos das colunas
                      auto_size_columns=False,          # Desativa auto-size para usar col_widths
                      col_widths=[10, 30],              # Largura das colunas (ID pequeno, Nome grande)
                      display_row_numbers=False,
                      justification='left',
                      num_rows=min(25, len(dados_tabela)),
                      key='-TABELA-',
                      row_height=35)],
            [sg.Button('Fechar')]
        ]

        # 3. Abre a Janela
        window = sg.Window('Listagem de Capitães', layout)
        window.read()
        window.close()

        return True

    def retorna(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        opcoes: dict[int, Any] = {1: self.inclui, 2: self.exclui, 3: self.lista, 0: self.retorna}
        continua = True
        while continua:
            escolha = self.__tela_capitao.abre_opcoes()
            opcoes[escolha]()