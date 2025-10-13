from typing import Any
from controle.gerador_id import GeradorId
from models.administrador import Administrador
from telas.tela_admin import TelaAdmin

class ControladorAdmin(GeradorId):
    def __init__(self, controlador_sistema):  # type: ignore
        self.__admins: list[Administrador] = []
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaAdmin()

        super().__init__(self.__admins)

    def inclui(self):
        dados = self.__tela.pega_dados()
        if not dados:
            return

        capitao = Administrador(self.gera_id(), dados['nome'], dados['telefone'])
        self.__admins.append(capitao)
        self.__tela.mostra_mensagem('Administrador adicionado com sucesso!')

    def pega_index_admin_por_id(self, id: int):
        for i in range(len(self.__admins)):
            if self.__admins[i].id == id:
                return i
            
        return None

    def exclui(self):
        self.__tela.mostra_titulo('Excluir Administrador')

        if not self.lista():
            return

        id = self.__tela.seleciona_id()
        if id is None:
            return

        index = self.pega_index_admin_por_id(id)
        if index is None:
            self.__tela.mostra_erro('Administrador não encontrado')
            return

        admin = self.__admins.pop(index)
        self.__tela.mostra_mensagem(f'Administrador {admin.nome} (ID: {admin.id}) removido com sucesso!')
        self.lista()

    def lista(self) -> bool:
        print('\nListando administradores...')

        if len(self.__admins) == 0:
            print('Nenhum administrador encontrado')
            return False

        for admin in self.__admins:
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