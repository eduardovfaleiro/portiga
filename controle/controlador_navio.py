from operator import attrgetter
from typing import Any
from controle.gerador_id import GeradorId
from models.carga import Carga
from models.navio import Navio
from telas.tela_navio import TelaNavio
from DAOs.navio_dao import NavioDAO

class ControladorNavio(GeradorId):
    def __init__(self, controlador_sistema): # type: ignore
        self.__navio_DAO = NavioDAO()
        self.__controlador_sistema = controlador_sistema
        self.__tela_navio = TelaNavio()
        super().__init__(self.__navio_DAO.get_all())

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

        novo_id = super().gera_id()
        navio = Navio(novo_id, dados['nome'], dados['bandeira'], companhia, capitao, [])
        self.__navio_DAO.add(navio) 
        self.__tela_navio.mostra_mensagem('Navio adicionado com sucesso!')

    def pega_navio_por_id(self, id: int) -> Navio | None:
        return self.__navio_DAO.get(id)

    def altera(self):
        self.__tela_navio.mostra_titulo('Alterar Navio')

        tem_navios = self.lista()
        if not tem_navios:
            return

        while True:
            id = self.__tela_navio.seleciona_navio()
            if id is None:
                return

            navio_atual = self.pega_navio_por_id(id)
            if navio_atual is None:
                self.__tela_navio.mostra_erro('Navio não existe.')
            else:
                break

        novos_dados = self.__tela_navio.pega_dados_opcionais_navio()
        if not novos_dados:
            return

        if novos_dados['nome'] is not None and novos_dados['nome'].strip() != '':
            navio_atual.nome = novos_dados['nome']

        if novos_dados['bandeira'] is not None:
            navio_atual.bandeira = novos_dados['bandeira']

        if novos_dados['companhia'] is not None:
            ctrl_comp = getattr(self.__controlador_sistema, 'controlador_companhia', None)
            if isinstance(novos_dados['companhia'], int) and ctrl_comp is not None and hasattr(ctrl_comp, 'pega_companhia_por_id'):
                navio_atual.companhia = ctrl_comp.pega_companhia_por_id(novos_dados['companhia'])

        if novos_dados.get('capitao') is not None:
            ctrl_cap = getattr(self.__controlador_sistema, 'controlador_capitao', None)
            if isinstance(novos_dados['capitao'], int) and ctrl_cap is not None and hasattr(ctrl_cap, 'pega_capitao_por_id'):
                navio_atual.capitao = ctrl_cap.pega_capitao_por_id(novos_dados['capitao'])

        self.__navio_DAO.update(navio_atual.id, navio_atual)
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
            
            navio = self.pega_navio_por_id(id)
            
            if navio is not None:
                self.__navio_DAO.remove(id)
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
                id_navio = self.__tela_navio.seleciona_navio()
                if id_navio is None:
                    return

                navio = self.pega_navio_por_id(id_navio) 
                
                if navio is None:
                    self.__tela_navio.mostra_erro('Navio não encontrado.')
                    continue
                else:
                    break

            produto = input('Produto: ').strip()
            if produto == '':
                self.__tela_navio.mostra_erro('Produto inválido.')
                return
                
            tipo_raw = input('Tipo: ').strip()
            try:
                tipo = int(tipo_raw)
                if tipo < 1 or tipo > 4:
                    self.__tela_navio.mostra_erro('Tipo deve ser um número entre 1 e 4.')
                    return
            except ValueError:
                self.__tela_navio.mostra_erro('Tipo inválido (deve ser um número inteiro).')
                return

            peso_raw = input('Peso (kg): ').strip()
            try:
                peso = float(peso_raw)
                if peso < 0:
                    raise ValueError()
            except Exception:
                self.__tela_navio.mostra_erro('Peso inválido.')
                return

            valor_raw = input('Valor (R$): ').strip()
            try:
                valor = float(valor_raw)
                if valor < 0:
                    raise ValueError()
            except Exception:
                self.__tela_navio.mostra_erro('Valor inválido.')
                return

            cargas_do_navio = getattr(navio, 'cargas', []) or []
            gerador = GeradorId(cargas_do_navio)
            novo_id = gerador.gera_id()
            novo_id_str = str(novo_id)

            try:
                carga = Carga(novo_id_str, produto, tipo, peso, valor)
            except Exception as e:
                self.__tela_navio.mostra_erro(f'Erro ao criar carga: {e}')
                return

            cargas_do_navio.append(carga)
            navio.cargas = cargas_do_navio
            
            self.__navio_DAO.update(navio.id, navio) 
            
            self.__controlador_sistema.controlador_relatorio.registra_carregamento(carga)

            self.__tela_navio.mostra_mensagem(f'Carga {carga.id} adicionada com sucesso!')
            self.lista()

    def descarrega(self):
        self.__tela_navio.mostra_titulo('Descarregar Navio')

        tem_navios = self.lista()
        if not tem_navios:
            return

        while True:
            id = self.__tela_navio.seleciona_navio()
            if id is None:
                return

            navio = self.pega_navio_por_id(id)
            if navio is None:
                self.__tela_navio.mostra_erro('Navio não existe para o id informado.')
                continue
            
            cargas = getattr(navio, 'cargas', []) or []
            if len(cargas) == 0:
                self.__tela_navio.mostra_erro('Este navio não possui cargas para descarregar.')
                return

            print('\nCargas embarcadas:')
            for c in cargas:
                cid = getattr(c, 'id', None) or getattr(c, 'codigo', '')
                cproduto = getattr(c, 'produto', '')
                ctipo = getattr(c, 'tipo', '')
                cpeso = getattr(c, 'peso', '')
                cvalor = getattr(c, 'valor', '')
                print(f'- {cid} | {cproduto} | {ctipo} | {cpeso} kg | R$ {cvalor}')

            codigo = self.__tela_navio.seleciona_carga()
            if codigo is None:
                return

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

            self.__navio_DAO.update(navio.id, navio)

            self.__controlador_sistema.controlador_relatorio.registra_descarregamento(carga_removida)

            self.__tela_navio.mostra_mensagem(f'Carga {getattr(carga_removida, "id", "")} removida com sucesso!')
            self.lista()

    def lista(self) -> bool:
        print('\nListando navios...')
        navios = self.__navio_DAO.get_all()
        if len(navios) == 0:
            print('Nenhum navio encontrado')
            return False

        for navio in navios:
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