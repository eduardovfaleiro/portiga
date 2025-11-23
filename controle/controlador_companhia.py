from typing import Any
from controle.gerador_id import GeradorId
from models.companhia import Companhia
from telas.tela_companhia import TelaCompanhia
from DAOs.companhia_dao import CompanhiaDAO

class ControladorCompanhia(GeradorId):
    def __init__(self, controlador_sistema: Any): # type: ignore
        self.__companhia_DAO = CompanhiaDAO()
        self.__controlador_sistema = controlador_sistema
        self.__tela_companhia = TelaCompanhia()
        super().__init__(self.__companhia_DAO.get_all())

    def inclui(self):
        dados = self.__tela_companhia.pega_dados_companhia()

        companhia = Companhia(self.gera_id(), dados['nome'], dados['pais_sede'])
        self.__companhia_DAO.add(companhia)
        self.__tela_companhia.mostra_mensagem('Companhia adicionada com sucesso!')

    def pega_companhia_por_id(self, id: int) -> Companhia | None:
        for i in range(len(self.__companhias)):
            if self.__companhias[i].id == id:
                return self.__companhias[i]
            
        return None

    def altera(self):
        self.__tela_companhia.mostra_titulo('Alterar Companhia')
        tem_companhias = self.lista()
        if not tem_companhias: return

        while True:
            id = self.__tela_companhia.seleciona_id()
            if id is None: return

            companhia_atual = self.pega_companhia_por_id(id)
            if companhia_atual is None:
                self.__tela_companhia.mostra_erro('Companhia não existe')
            else:
                break
        
        novos_dados = self.__tela_companhia.pega_dados_opcionais_companhia()
        
        if novos_dados['nome'] != None and novos_dados['nome'].strip() != '': # Fixed .strip() call
            companhia_atual.nome = novos_dados['nome']

        if novos_dados['pais_sede'] != None:
            companhia_atual.pais_sede = novos_dados['pais_sede']

        self.__companhia_DAO.update(companhia_atual.id, companhia_atual)
        self.__tela_companhia.mostra_mensagem(f'Companhia {companhia_atual.id} alterada com sucesso!')

    def exclui(self):
        self.__tela_companhia.mostra_titulo('Excluir Companhia')

        tem_companhias = self.lista()
        if not tem_companhias: return

        while True:
            id = self.__tela_companhia.seleciona_id()
            if id is None: return

            companhia_a_excluir = self.__companhia_DAO.get(id)
            
            if companhia_a_excluir is None:
                self.__tela_companhia.mostra_erro('Companhia não existe')
            else:
                self.__companhia_DAO.remove(id)
                self.__tela_companhia.mostra_mensagem(f'Companhia {companhia_a_excluir.nome} (ID: {companhia_a_excluir.id}) excluída com sucesso!')
                self.lista()
                return

    def lista(self) -> bool:
        print('\nListando companhias...')

        companhias = self.__companhia_DAO.get_all()

        if len(companhias) == 0:
            print('Nenhuma companhia encontrada')
            return False
        
        for companhia in companhias:
            self.__tela_companhia.mostra_mensagem(f'{companhia.__str__()}')
        
        return True

    def retorna(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        opcoes: dict[int, Any] = {1: self.inclui, 2: self.exclui, 3: self.altera, 4: self.lista, 0: self.retorna}

        continua = True
        while continua:
            opcoes[self.__tela_companhia.abre_opcoes()]()