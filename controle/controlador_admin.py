from typing import Any
from controle.gerador_id import GeradorId
from models.administrador import Administrador
from telas.tela_admin import TelaAdmin
from DAOs.administrador_dao import AdministradorDAO

class ControladorAdmin(GeradorId):
    def __init__(self, controlador_sistema):  # type: ignore
        self.__administrador_DAO = AdministradorDAO()
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaAdmin()
        super().__init__(self.__administrador_DAO.get_all())

    def inclui(self):
        dados = self.__tela.pega_dados()
        if not dados:
            return

        administrador = Administrador(self.gera_id(), dados['nome'], dados['telefone'])
        self.__administrador_DAO.add(administrador)
        self.__tela.mostra_mensagem('Administrador adicionado com sucesso!')

    def exclui(self):
        self.__tela.mostra_titulo('Excluir Administrador')

        if not self.lista():
            return

        administrador_id = self.__tela.seleciona_id()
        if administrador_id is None:
            return

        administrador = self.__administrador_DAO.get(administrador_id)

        if administrador is None:
            self.__tela.mostra_erro('Administrador não encontrado')
            return
        
        self.__administrador_DAO.remove(administrador_id)
        self.__tela.mostra_mensagem(f'Administrador {administrador.nome} (ID: {administrador.id}) removido com sucesso!')
        self.lista()

    def lista(self) -> bool:
        print('\nListando administradores...')
        administradores = self.__administrador_DAO.get_all()

        if len(administradores) == 0:
            print('Nenhum administrador encontrado')
            return False

        for admin in administradores:
            print(f'{admin}\n')

        return True

    def retorna(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        opcoes: dict[int, Any] = {1: self.inclui, 2: self.exclui, 3: self.lista, 0: self.retorna}
        continua = True
        while continua:
            escolha = self.__tela.abre_opcoes()
            opcoes[escolha]()