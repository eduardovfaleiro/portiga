from typing import Any
from controle.gerador_id import GeradorId
from entidade.administrador import Administrador
from tela.tela_admin import TelaAdmin
from DAOs.administrador_dao import AdministradorDAO
import FreeSimpleGUI as sg

class ControladorAdmin(GeradorId):
    def __init__(self, controlador_sistema):  # type: ignore
        self.__administrador_DAO = AdministradorDAO()
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaAdmin()
        super().__init__(self.__administrador_DAO.get_all())

    def pega_por_id(self, id: int):
        return self.__administrador_DAO.get(id)


    def inclui(self):
        dados = self.__tela.pega_dados()
        if not dados:
            return

        administrador = Administrador(self.gera_id(), dados['nome'], dados['telefone'])
        self.__administrador_DAO.add(administrador)
        self.__tela.mostra_mensagem('Administrador adicionado com sucesso!')

    def exclui(self):
        has_admin = self.lista()
        
        if not has_admin:
            return

        # 2. Abre a janelinha pedindo o ID (implementada acima)
        administrador_id = self.__tela.seleciona_id()
        
        if administrador_id is None:
            return # Usuário clicou em cancelar ou fechou a janela

        # 3. Busca no banco de dados (DAO)
        administrador = self.__administrador_DAO.get(administrador_id)

        if administrador is None:
            self.__tela.mostra_erro('Administrador não encontrado para o ID informado.')
            return
        
        # 4. Remove e dá feedback
        self.__administrador_DAO.remove(administrador_id)
        self.__tela.mostra_mensagem(f'Administrador {administrador.nome} removido com sucesso!')
        
        # 5. Lista novamente para confirmar visualmente a exclusão
        self.lista()

    def lista(self) -> bool:
    # 1. Busca os dados (mantém sua lógica original)
        administradores = self.__administrador_DAO.get_all()

        if len(administradores) == 0:
            sg.popup('Nenhum administrador encontrado.')
            return False

        # 2. Transforma Objetos em Lista de Listas para o FreeSimpleGUI
        # Assumindo que seu objeto Admin tem .nome e .telefone
        # Se não tiver atributos diretos, ajuste para admin.id, etc.
        dados_tabela = []
        for admin in administradores:
            # Cria uma linha com as colunas que você quer mostrar
            dados_tabela.append([admin.id, admin.nome, admin.telefone])

        # 3. Define o Layout com a Tabela
        layout = [
            [sg.Text('Lista de Administradores', font=('Helvetica', 15))],
            [sg.Table(values=dados_tabela,
                      headings=['ID', 'Nome', 'Telefone'], # Cabeçalhos das colunas
                      auto_size_columns=True,
                      display_row_numbers=False,
                      justification='left',
                      num_rows=min(25, len(dados_tabela)), # Altura dinâmica
                      key='-TABELA-',
                      row_height=35)],
            [sg.Button('Fechar')]
        ]

        # 4. Abre a janela
        window = sg.Window('Listagem', layout)
        window.read()
        window.close()

        return True

    def retorna(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        opcoes: dict[int, Any] = {1: self.inclui, 2: self.exclui, 3: self.lista, 0: self.retorna}
        continua = True
        while continua:
            escolha = self.__tela.abre_opcoes()
            opcoes[escolha]()