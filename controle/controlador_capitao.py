from operator import attrgetter
from typing import Any
from controle.gerador_id import GeradorId
from models.capitao import Capitao
from telas.tela_capitao import TelaCapitao

class ControladorCapitao(GeradorId):
    def __init__(self, controlador_sistema):  # type: ignore
        self.__capitaes: list[Capitao] = []
        self.__controlador_sistema = controlador_sistema
        self.__tela_capitao = TelaCapitao()

        super().__init__(self.__capitaes)

    def inclui(self):
        dados = self.__tela_capitao.pega_dados_capitao()
        if not dados:
            return

        capitao = Capitao(self.gera_id(), dados['nome'])
        self.__capitaes.append(capitao)
        self.__tela_capitao.mostra_mensagem('Capitão adicionado com sucesso!')

    def pega_index_capitao_por_id(self, id: int):
        for i in range(len(self.__capitaes)):
            if self.__capitaes[i].id == id:
                return i
            
        return None

    def pega_capitao_por_id(self, id: int):
        idx = self.pega_index_capitao_por_id(id)
        if idx is None:
            return None
        return self.__capitaes[idx]

    def exclui(self):
        self.__tela_capitao.mostra_titulo('Excluir Capitão')

        if not self.lista():
            return

        selecionado = self.__tela_capitao.seleciona_capitao()  # espera ID
        if selecionado is None:
            return

        index = self.pega_index_capitao_por_id(selecionado)
        if index is None:
            self.__tela_capitao.mostra_erro('Capitão não encontrado')
            return

        capitao = self.__capitaes.pop(index)
        self.__tela_capitao.mostra_mensagem(f'Capitão {capitao.nome} (ID: {capitao.id}) removido com sucesso!')
        self.lista()

    def lista(self) -> bool:
        print('\nListando capitães...')

        if len(self.__capitaes) == 0:
            print('Nenhum capitão encontrado')
            return False

        for capitao in self.__capitaes:
            self.__tela_capitao.mostra_capitao(capitao)

        return True

    def retorna(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        opcoes: dict[int, Any] = {1: self.inclui, 2: self.exclui, 3: self.lista, 0: self.retorna}
        continua = True
        while continua:
            escolha = self.__tela_capitao.abre_opcoes()
            opcoes[escolha]()