from operator import attrgetter
from typing import Any
from models.companhia import Companhia
from telas.tela_companhia import TelaCompanhia

class ControladorCompanhia:
    def __init__(self, controlador_sistema): # type: ignore
        self.__companhias: list[Companhia] = []
        self.__controlador_sistema = controlador_sistema
        self.__tela_companhia = TelaCompanhia()

    def gera_id(self) -> int:
        if len(self.__companhias) == 0:
            return 0

        ultimo_id = max(self.__companhias, key=attrgetter('id')).id
        novo_id = ultimo_id + 1
        return novo_id

    def inclui(self):
        dados = self.__tela_companhia.pega_dados_companhia()

        companhia = Companhia(self.gera_id(), dados['nome'], dados['pais_sede'])
        self.__companhias.append(companhia)
        self.__tela_companhia.mostra_mensagem('Companhia adicionada com sucesso!')

    def pega_index_companhia_por_id(self, id: int):
        for i in range(len(self.__companhias)):
            if self.__companhias[i].id == id:
                return i
            
        return None

    def altera(self):
        self.__tela_companhia.mostra_titulo('Alterar Companhia')
        
        existem_companhias = self.lista()
        if not existem_companhias:
            self.__tela_companhia.mostra_erro('Nenhuma companhia encontrada')
            return

        id = self.__tela_companhia.seleciona_companhia()

        index = self.pega_index_companhia_por_id(id)
        if index is None:
            self.__tela_companhia.mostra_mensagem('ERRO: Companhia não existente')
            return
        
        novos_dados = self.__tela_companhia.pega_dados_opcionais_companhia()
        
        companhia_atual = self.__companhias[index]
        self.__companhias[index] = companhia_atual.copyWith(nome=novos_dados['nome'], pais_sede=novos_dados['pais_sede'])
        self.__tela_companhia.mostra_mensagem(f'Companhia {companhia_atual.id} alterada com sucesso!')

    def exclui(self):
        self.lista()
        id = self.__tela_companhia.seleciona_companhia()
        
        for i in range(len(self.__companhias)):
            if self.__companhias[i].id == id:
                self.__companhias.pop(i)
                self.lista()
                return
                
        self.__tela_companhia.mostra_mensagem('ERRO: Companhia não existente')

    def lista(self) -> bool:
        print('Listando companhias...')

        if len(self.__companhias) == 0:
            print('Nenhuma companhia encontrada')
            return False
        
        for companhia in self.__companhias:
            self.__tela_companhia.mostra_companhia(companhia)
        
        return True

    def retorna(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        opcoes: dict[int, Any] = {1: self.inclui, 2: self.exclui, 3: self.altera, 4: self.lista, 0: self.retorna}

        continua = True
        while continua:
            opcoes[self.__tela_companhia.abre_opcoes()]()