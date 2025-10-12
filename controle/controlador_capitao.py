from operator import attrgetter
from typing import Any
from models.capitao import Capitao
from telas.tela_capitao import TelaCapitao

class ControladorCapitao:
    def __init__(self, controlador_sistema):  # type: ignore
        self.__capitaes: list[Capitao] = []
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaCapitao()

    def gera_id(self) -> int:
        if len(self.__capitaes) == 0:
            return 0
        ultimo_id = max(self.__capitaes, key=attrgetter('id')).id if hasattr(self.__capitaes[0], 'id') else len(self.__capitaes) - 1
        return ultimo_id + 1
    
    def pega_capitao_por_id(self, id: int):
        """Retorna instância de Capitao pelo atributo id, ou None."""
        for capitao in self.__capitaes:
            if hasattr(capitao, 'id') and getattr(capitao, 'id') == id:
                return capitao
        return None

    def inclui(self):
        dados = self.__tela.pega_dados_capitao()
        if not dados:
            return

        nome = dados.get('nome')
        if not nome or str(nome).strip() == '':
            self.__tela.mostra_erro('Nome inválido')
            return

        # Ajuste abaixo se Capitao aceita (id, nome) ou apenas nome.
        try:
            # tenta criar com id + nome (se seu modelo usar id)
            capitao = Capitao(self.gera_id(), nome)  # ajustar se necessário
        except TypeError:
            # fallback: tentar apenas nome
            capitao = Capitao(nome)

        self.__capitaes.append(capitao)
        self.__tela.mostra_mensagem('Capitão adicionado com sucesso!')

    def exclui(self):
        self.__tela.mostra_titulo('Excluir Capitão')

        if not self.lista():
            return

        while True:
            selecionado = self.__tela.seleciona_capitao()
            if selecionado is None:
                return

            if not isinstance(selecionado, int):
                self.__tela.mostra_erro('Seleção inválida. Informe o índice mostrado na lista.')
                continue

            if 0 <= selecionado < len(self.__capitaes):
                capitao = self.__capitaes.pop(selecionado)
                self.__tela.mostra_mensagem(f'Capitão removido com sucesso: {getattr(capitao, "nome", str(capitao))}')
                self.lista()
                return

            self.__tela.mostra_erro('Capitão não existe para o índice informado.')

    def lista(self) -> bool:
        print('\nListando capitães...')

        if len(self.__capitaes) == 0:
            print('Nenhum capitão encontrado')
            return False

        for i, capitao in enumerate(self.__capitaes):
            print(f'[{i}]', end=' ')
            try:
                self.__tela.mostra_capitao(capitao, i)
            except TypeError:
                # se tela espera só o objeto
                self.__tela.mostra_capitao(capitao)

        return True

    def retorna(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        opcoes: dict[int, Any] = {1: self.inclui, 2: self.exclui, 3: self.lista, 0: self.retorna}
        continua = True
        while continua:
            escolha = self.__tela.abre_opcoes()
            opcoes[escolha]()