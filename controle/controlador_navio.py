from operator import attrgetter
from typing import Any
from controle.gerador_id import GeradorId
from models.carga import Carga
from models.navio import Navio
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

        novo_id = self.gera_id()
        navio = Navio(novo_id, dados['nome'], dados['bandeira'], companhia, capitao, [])
        self.__navios.append(navio)
        self.__tela_navio.mostra_mensagem('Navio adicionado com sucesso!')

    def pega_navio_por_id(self, id: int) -> Navio | None:
        for i in range(len(self.__navios)):
            if self.__navios[i].id == id:
                return self.__navios[i]

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

            index = self.pega_navio_por_id(selecionado)
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

            index = self.pega_navio_por_id(id)
            if index is not None:
                navio = self.__navios.pop(index)
                self.__tela_navio.mostra_mensagem(f'Navio {navio.id} excluído com sucesso!')
                self.lista()
                return

            self.__tela_navio.mostra_erro('Navio não encontrado')
            
    def carrega(self):
        self.__tela_navio.mostra_titulo('Carregar Navio')

        tem_navios = self.lista()
        if not tem_navios:
            return

        while True:
            id = self.__tela_navio.seleciona_navio()
            if id is None:
                return

            index = self.pega_navio_por_id(id)
            navio = self.__navios[id]

            # tipo
            tipo = input('Tipo da carga: ').strip()
            if tipo == '':
                self.__tela_navio.mostra_erro('Tipo inválido.')
                return

            # peso
            peso_raw = input('Peso (kg): ').strip()
            try:
                peso = float(peso_raw)
                if peso < 0:
                    raise ValueError()
            except Exception:
                self.__tela_navio.mostra_erro('Peso inválido.')
                return

            # valor
            valor_raw = input('Valor (R$): ').strip()
            try:
                valor = float(valor_raw)
                if valor < 0:
                    raise ValueError()
            except Exception:
                self.__tela_navio.mostra_erro('Valor inválido.')
                return

            # gerar id para a carga usando GeradorId sobre as cargas do próprio navio
            cargas_do_navio = getattr(navio, 'cargas', []) or []
            gerador = GeradorId(cargas_do_navio)
            novo_id = gerador.gera_id()
            novo_id_str = str(novo_id)

            # criar e anexar a carga ao navio
            try:
                carga = Carga(novo_id_str, tipo, peso, valor)
            except Exception as e:
                self.__tela_navio.mostra_erro(f'Erro ao criar carga: {e}')
                return

            # compatibilidade: expor atributo 'codigo' se algum trecho do código usar isso
            try:
                setattr(carga, 'codigo', carga.id)
            except Exception:
                pass

            navio.cargas = cargas_do_navio + [carga]
            self.__tela_navio.mostra_mensagem(f'Carga {carga.id} adicionada ao navio {navio.id}.')
            return
        
    def descarrega(self):
        self.__tela_navio.mostra_titulo('Descarregar Navio')

        tem_navios = self.lista()
        if not tem_navios:
            return

        while True:
            id = self.__tela_navio.seleciona_navio()
            if id is None:
                return

            index = self.pega_navio_por_id(id)
            if index is None:
                self.__tela_navio.mostra_erro('Navio não existe para o id informado.')
                continue
            navio = self.__navios[id]

            cargas = getattr(navio, 'cargas', []) or []
            if len(cargas) == 0:
                self.__tela_navio.mostra_erro('Este navio não possui cargas para descarregar.')
                return

            # listar cargas embarcadas
            print('\nCargas embarcadas:')
            for c in cargas:
                cid = getattr(c, 'id', None) or getattr(c, 'codigo', '')
                ctipo = getattr(c, 'tipo', '')
                cpeso = getattr(c, 'peso', '')
                cvalor = getattr(c, 'valor', '')
                print(f'- {cid} | {ctipo} | {cpeso} kg | R$ {cvalor}')

            # solicitar código/id da carga a remover via tela
            codigo = self.__tela_navio.seleciona_carga()
            if codigo is None:
                return

            # localizar carga no navio
            idx_remover = None
            for i, c in enumerate(cargas):
                if str(getattr(c, 'id', '')) == codigo or str(getattr(c, 'codigo', '')) == codigo:
                    idx_remover = i
                    break

            if idx_remover is None:
                self.__tela_navio.mostra_erro('Carga não encontrada.')
                continue

            carga_removida = cargas.pop(idx_remover)
            navio.cargas = list(cargas)
            self.__tela_navio.mostra_mensagem(f'Carga {getattr(carga_removida, "id", "")} descarregada do navio {navio.id}.')
            return

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
        opcoes: dict[int, Any] = {1: self.inclui, 2: self.exclui, 3: self.altera, 4: self.lista, 5:self.carrega, 6: self.descarrega, 0: self.retorna}

        continua = True
        while continua:
            escolha = self.__tela_navio.abre_opcoes()
            opcoes[escolha]()