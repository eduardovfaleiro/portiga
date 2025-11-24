from typing import Any
from entidade.carga import Carga
from tela.tela_carga import TelaCarga

class ControladorCarga:
    def __init__(self, controlador_sistema):  # type: ignore
        self.__cargas: list[Carga] = []
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaCarga()

    def pega_index_carga_por_id(self, id: str) -> int | None:
        for i, carga in enumerate(self.__cargas):
            if getattr(carga, 'id', None) == id:
                return i
        return None

    def pega_carga_por_id(self, id: str) -> Carga | None:
        idx = self.pega_index_carga_por_id(id)
        if idx is None:
            return None
        return self.__cargas[idx]

    def inclui(self):
        dados = self.__tela.pega_dados_carga()
        if dados is None:
            return

        id = dados.get('id')
        produto = dados.get('produto')
        tipo = dados.get('tipo')
        peso = dados.get('peso')
        valor = dados.get('valor')

        # validações mínimas
        if not isinstance(id, str) or id.strip() == '':
            self.__tela.mostra_erro('Código inválido')
            return

        if self.pega_carga_por_id(id) is not None:
            self.__tela.mostra_erro('Já existe carga com esse código')
            return

        try:
            carga = Carga(id.strip(), produto.strip(), tipo.strip(), float(peso), float(valor))
        except Exception as e:
            self.__tela.mostra_erro(f'Erro ao criar carga: {e}')
            return

        self.__cargas.append(carga)
        self.__tela.mostra_mensagem('Carga adicionada com sucesso!')

    def exclui(self):
        if not self.lista():
            return

        id = self.__tela.seleciona_carga()
        if id is None:
            return

        index = self.pega_index_carga_por_id(id)
        if index is None:
            self.__tela.mostra_erro('Carga não encontrada')
            return

        carga = self.__cargas.pop(index)
        self.__tela.mostra_mensagem(f'Carga {getattr(carga, "id", "")} excluída com sucesso!')
        self.lista()

    def lista(self) -> bool:
        if len(self.__cargas) == 0:
            print('\nNenhuma carga encontrada')
            return False

        print('\nListando cargas...')
        for carga in self.__cargas:
            self.__tela.mostra_carga(carga)
        return True

    def retorna(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        opcoes: dict[int, Any] = {1: self.inclui, 2: self.exclui, 3: self.lista, 0: self.retorna}
        while True:
            escolha = self.__tela.abre_opcoes()
            opcoes[escolha]()