from operator import attrgetter
from typing import Any
from controle.gerador_id import GeradorId
from entidade.carga import Carga
from entidade.navio import Navio
from tela.tela_navio import TelaNavio
from DAOs.navio_dao import NavioDAO
import FreeSimpleGUI as sg

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

        companhia = None
        if isinstance(dados.get('companhia'), int):
            ctrl_comp = getattr(self.__controlador_sistema, 'controlador_companhia', None)
            if ctrl_comp is not None and hasattr(ctrl_comp, 'pega_companhia_por_id'):
                companhia = ctrl_comp.pega_companhia_por_id(dados['companhia'])

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

        self.__navio_DAO.update(navio_atual)
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
        if not self.lista():
            return

        while True:
            id_navio = self.__tela_navio.seleciona_navio()
            
            if id_navio is None:
                return

            navio = self.pega_navio_por_id(id_navio) 
            
            if navio is None:
                self.__tela_navio.mostra_erro('Navio não encontrado. Tente novamente.')
                continue
            else:
                break

        dados_carga = self.__tela_navio.pega_dados_carga()
        
        if dados_carga is None:
            return

        produto = dados_carga['produto']
        tipo = dados_carga['tipo']
        peso = dados_carga['peso']
        valor = dados_carga['valor']

        cargas_do_navio = getattr(navio, 'cargas', []) or []
        
        gerador = GeradorId(cargas_do_navio)
        novo_id = gerador.gera_id()
        novo_id_str = str(novo_id)

        try:
            carga = Carga(novo_id_str, produto, tipo, peso, valor)
        except Exception as e:
            self.__tela_navio.mostra_erro(f'Erro de validação na classe Carga: {e}')
            return

        cargas_do_navio.append(carga)
        navio.cargas = cargas_do_navio
        
        self.__navio_DAO.update(navio) 
        
        self.__controlador_sistema.controlador_relatorio.registra_carregamento(carga)

        self.__tela_navio.mostra_mensagem(f'Carga {carga.id} adicionada ao navio {navio.nome} com sucesso!')
        
        self.lista()

    def descarrega(self):
        tem_navios = self.lista()
        if not tem_navios:
            return

        while True:
            id_navio = self.__tela_navio.seleciona_navio()
            if id_navio is None:
                return

            navio = self.pega_navio_por_id(id_navio)
            if navio is None:
                self.__tela_navio.mostra_erro('Navio não existe para o id informado.')
                continue
            
            cargas = getattr(navio, 'cargas', []) or []
            if len(cargas) == 0:
                self.__tela_navio.mostra_erro('Este navio não possui cargas para descarregar.')
                return

            self.__tela_navio.mostra_cargas_navio(cargas)

            codigo = self.__tela_navio.seleciona_carga()
            if codigo is None:
                return

            idx_remover = None
            for i, c in enumerate(cargas):
                c_id = str(getattr(c, 'id', ''))
                c_cod = str(getattr(c, 'codigo', ''))
                if c_id == codigo or c_cod == codigo:
                    idx_remover = i
                    break

            if idx_remover is None:
                self.__tela_navio.mostra_erro('Carga não encontrada com este ID dentro deste navio.')
                continue

            carga_removida = cargas.pop(idx_remover)
            
            navio.cargas = list(cargas)
            self.__navio_DAO.update(navio)
            self.__controlador_sistema.controlador_relatorio.registra_descarregamento(carga_removida)
            self.__tela_navio.mostra_mensagem(f'Carga {getattr(carga_removida, "id", "")} removida com sucesso!')
            self.lista()
            break

    def lista(self) -> bool:
        navios = self.__navio_DAO.get_all()
        
        if len(navios) == 0:
            sg.popup('Nenhum navio encontrado', title='Aviso')
            return False

        texto_relatorio = ""
        
        for navio in navios:
            if isinstance(navio, dict):
                id_ = navio.get('id', '')
                nome = navio.get('nome', '')
                bandeira = navio.get('bandeira')
                companhia = navio.get('companhia')
                capitao = navio.get('capitao')
                cargas = navio.get('cargas', [])
            else:
                id_ = getattr(navio, 'id', '')
                nome = getattr(navio, 'nome', '')
                bandeira = getattr(navio, 'bandeira', None)
                companhia = getattr(navio, 'companhia', None)
                capitao = getattr(navio, 'capitao', None)
                cargas = getattr(navio, 'cargas', [])

            bandeira_txt = bandeira.codigo if bandeira else 'N/A'
            companhia_txt = companhia.nome if companhia else 'N/A'
            capitao_txt = capitao.nome if capitao else 'N/A'

            texto_relatorio += "="*60 + "\n"
            texto_relatorio += f"🚢 NAVIO [{id_}]: {nome}\n"
            texto_relatorio += f"   Bandeira: {bandeira_txt} | Cia: {companhia_txt} | Cap: {capitao_txt}\n"
            texto_relatorio += "-"*60 + "\n"

            if not cargas:
                texto_relatorio += "   [Sem cargas carregadas]\n"
            else:
                texto_relatorio += "   📦 CARGAS A BORDO:\n"
                for c in cargas:
                    cid = getattr(c, 'id', '')
                    cprod = getattr(c, 'produto', '')
                    ctipo = getattr(c, 'tipo', '')
                    cpeso = getattr(c, 'peso', 0)
                    cvalor = getattr(c, 'valor', 0)
                    
                    texto_relatorio += (f"   • ID: {cid} | Produto: {cprod} (Tipo {ctipo})\n"
                                        f"     Peso: {cpeso} kg | Valor: R$ {cvalor:.2f}\n")
                    texto_relatorio += "     " + "."*40 + "\n"

            texto_relatorio += "\n"

        layout = [
            [sg.Text('Relatório Detalhado de Navios e Cargas', font=('Helvetica', 16))],
            [sg.Multiline(texto_relatorio, 
                          size=(80, 20),
                          font=('Courier', 10),
                          disabled=True,
                          autoscroll=True)],
            [sg.Button('Fechar', size=(10,1))]
        ]

        window = sg.Window('Listagem Completa', layout)
        window.read()
        window.close()

        return True
    def retorna(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        opcoes: dict[int, Any] = {1: self.inclui, 2: self.exclui, 3: self.altera, 4: self.lista, 5:self.carrega, 6: self.descarrega, 0: self.retorna}

        continua = True
        while continua:
            escolha = self.__tela_navio.abre_opcoes()
            opcoes[escolha]()