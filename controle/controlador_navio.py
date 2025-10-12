from operator import attrgetter
from typing import Any
from models.navio import Navio
from models.carga import Carga
from telas.tela_navio import TelaNavio

class ControladorNavio:
    def __init__(self, controlador_sistema): # type: ignore
        self.__navios: list[Navio] = []
        self.__controlador_sistema = controlador_sistema
        self.__tela_navio = TelaNavio()

    def gera_id(self) -> int:
        if len(self.__navios) == 0:
            return 0

        ultimo_id = max(self.__navios, key=attrgetter('id')).id
        novo_id = ultimo_id + 1
        return novo_id

    def inclui(self):
        dados = self.__tela_navio.pega_dados_navio()
        if dados is None:
            return

        # converte companhia id -> instância (se fornecido)
        companhia = None
        if isinstance(dados.get('companhia'), int):
            ctrl_comp = getattr(self.__controlador_sistema, 'controlador_companhia', None)
            if ctrl_comp is not None and hasattr(ctrl_comp, 'pega_companhia_por_id'):
                companhia = ctrl_comp.pega_companhia_por_id(dados['companhia'])

        # converte capitao id -> instância (se fornecido)
        capitao = None
        if isinstance(dados.get('capitao'), int):
            ctrl_cap = getattr(self.__controlador_sistema, 'controlador_capitao', None)
            if ctrl_cap is not None and hasattr(ctrl_cap, 'pega_capitao_por_id'):
                capitao = ctrl_cap.pega_capitao_por_id(dados['capitao'])

        # converte lista de strings -> instâncias de Carga
        cargas_input = dados.get('cargas', []) or []
        cargas_inst: list[Carga] = []
        for desc in cargas_input:
            if not isinstance(desc, str):
                continue
            texto = desc.strip()
            if texto == '':
                continue
            try:
                cargas_inst.append(Carga(texto))
            except TypeError:
                try:
                    cargas_inst.append(Carga(descricao=texto))
                except TypeError:
                    raise

        novo_id = self.gera_id()
        navio = Navio(novo_id, dados['nome'], dados['bandeira'], companhia, capitao, cargas_inst)
        self.__navios.append(navio)
        self.__tela_navio.mostra_mensagem('Navio adicionado com sucesso!')

    def pega_index_navio_por_id(self, id: int):
        for i in range(len(self.__navios)):
            if self.__navios[i].id == id:
                return i
        return None

    def altera(self):
        self.__tela_navio.mostra_titulo('Alterar Navio')

        tem_navios = self.lista()
        if not tem_navios:
            return

        while True:
            selecionado = self.__tela_navio.seleciona_navio()
            if selecionado is None:
                return

            if not isinstance(selecionado, int):
                self.__tela_navio.mostra_erro('Seleção inválida. Forneça o id do navio.')
                continue

            index = self.pega_index_navio_por_id(selecionado)
            if index is None:
                self.__tela_navio.mostra_erro('Navio não existe para o id informado.')
            else:
                break

        novos_dados = self.__tela_navio.pega_dados_opcionais_navio()
        if not novos_dados:
            return

        navio_atual = self.__navios[index]

        # nome
        if novos_dados.get('nome') is not None and str(novos_dados.get('nome')).strip() != '':
            navio_atual.nome = novos_dados['nome']

        # bandeira (Tela retorna Pais ou None)
        if novos_dados.get('bandeira') is not None:
            navio_atual.bandeira = novos_dados['bandeira']

        # companhia (id -> instância)
        if novos_dados.get('companhia') is not None:
            ctrl_comp = getattr(self.__controlador_sistema, 'controlador_companhia', None)
            if isinstance(novos_dados['companhia'], int) and ctrl_comp is not None and hasattr(ctrl_comp, 'pega_companhia_por_id'):
                navio_atual.companhia = ctrl_comp.pega_companhia_por_id(novos_dados['companhia'])

        # capitao (id -> instância)
        if novos_dados.get('capitao') is not None:
            ctrl_cap = getattr(self.__controlador_sistema, 'controlador_capitao', None)
            if isinstance(novos_dados['capitao'], int) and ctrl_cap is not None and hasattr(ctrl_cap, 'pega_capitao_por_id'):
                navio_atual.capitao = ctrl_cap.pega_capitao_por_id(novos_dados['capitao'])

        # cargas (lista de strings -> lista de Carga)
        if novos_dados.get('cargas') is not None:
            entradas = novos_dados['cargas']
            if isinstance(entradas, list):
                cargas_limpa = [c.strip() for c in entradas if isinstance(c, str) and c.strip() != '']
                navio_atual.cargas = [Carga(descricao=c) for c in cargas_limpa]
            else:
                if isinstance(entradas, str) and entradas.strip() != '':
                    navio_atual.cargas = [Carga(descricao=entradas.strip())]

        self.__tela_navio.mostra_mensagem(f'Navio {navio_atual.id} alterado com sucesso!')

    def exclui(self):
        self.__tela_navio.mostra_titulo('Excluir Navio')

        tem_navios = self.lista()
        if not tem_navios:
            return

        while True:
            id = self.__tela_navio.seleciona_navio()
            if id is None:
                return

            index = self.pega_index_navio_por_id(id)
            if index is not None:
                navio = self.__navios.pop(index)
                self.__tela_navio.mostra_mensagem(f'Navio {navio.id} excluído com sucesso!')
                self.lista()
                return

            self.__tela_navio.mostra_erro('Navio não encontrado')

    def lista(self) -> bool:
        print('\nListando navios...')

        if len(self.__navios) == 0:
            print('Nenhum navio encontrado')
            return False

        for navio in self.__navios:
            self.__tela_navio.mostra_navio(navio)

        return True

    def retorna(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        opcoes: dict[int, Any] = {1: self.inclui, 2: self.exclui, 3: self.altera, 4: self.lista, 0: self.retorna}

        continua = True
        while continua:
            escolha = self.__tela_navio.abre_opcoes()
            opcoes[escolha]()