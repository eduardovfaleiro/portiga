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
        # 1. Mostra a lista para o usuário saber qual ID escolher
        # Se não houver navios, lista() retorna False e paramos aqui.
        if not self.lista():
            return

        # 2. Loop de Seleção do Navio
        while True:
            id_navio = self.__tela_navio.seleciona_navio()
            
            # Se retornou None, o usuário clicou em Cancelar ou fechou a janela
            if id_navio is None:
                return

            navio = self.pega_navio_por_id(id_navio) 
            
            if navio is None:
                self.__tela_navio.mostra_erro('Navio não encontrado. Tente novamente.')
                continue # Volta para o loop para pedir o ID de novo
            else:
                break # Navio válido encontrado

        # 3. Coleta os dados da Carga (Abre janela de formulário)
        # A validação de tipos (int/float) já foi feita dentro deste método na Tela
        dados_carga = self.__tela_navio.pega_dados_carga()
        
        if dados_carga is None:
            return # Usuário cancelou o formulário

        # 4. Extrai dados validados
        produto = dados_carga['produto']
        tipo = dados_carga['tipo'] # Já vem como int (1-4)
        peso = dados_carga['peso'] # Já vem como float
        valor = dados_carga['valor'] # Já vem como float

        # 5. Lógica de Negócio (Geração de ID)
        cargas_do_navio = getattr(navio, 'cargas', []) or []
        
        # Assumindo que GeradorId existe e funciona como no código original
        gerador = GeradorId(cargas_do_navio)
        novo_id = gerador.gera_id()
        novo_id_str = str(novo_id)

        try:
            # Criação do Objeto
            carga = Carga(novo_id_str, produto, tipo, peso, valor)
        except Exception as e:
            self.__tela_navio.mostra_erro(f'Erro de validação na classe Carga: {e}')
            return

        # 6. Persistência
        cargas_do_navio.append(carga)
        navio.cargas = cargas_do_navio
        
        self.__navio_DAO.update(navio) 
        
        # 7. Integração com Relatórios
        self.__controlador_sistema.controlador_relatorio.registra_carregamento(carga)

        # 8. Feedback Final
        self.__tela_navio.mostra_mensagem(f'Carga {carga.id} adicionada ao navio {navio.nome} com sucesso!')
        
        # Mostra a lista atualizada (opcional, mas bom para confirmar visualmente)
        self.lista()

    def descarrega(self):
        # 1. Abre a lista geral de navios para o usuário ver os IDs
        tem_navios = self.lista()
        if not tem_navios:
            return

        while True:
            # 2. Pede o ID do Navio
            id_navio = self.__tela_navio.seleciona_navio()
            if id_navio is None:
                return # Cancelou

            navio = self.pega_navio_por_id(id_navio)
            if navio is None:
                self.__tela_navio.mostra_erro('Navio não existe para o id informado.')
                continue # Pede de novo
            
            # 3. Verifica cargas
            cargas = getattr(navio, 'cargas', []) or []
            if len(cargas) == 0:
                self.__tela_navio.mostra_erro('Este navio não possui cargas para descarregar.')
                return # Retorna ao menu pois não há o que fazer

            # 4. GUI: Mostra a tabela de cargas DESTE navio
            # (Substitui o loop de prints do código original)
            self.__tela_navio.mostra_cargas_navio(cargas)

            # 5. Pede o ID da Carga
            codigo = self.__tela_navio.seleciona_carga()
            if codigo is None:
                return # Cancelou a seleção da carga

            # 6. Lógica de busca e remoção (Mantida idêntica)
            idx_remover = None
            for i, c in enumerate(cargas):
                # Compara ID (suportando atributo 'id' ou 'codigo')
                c_id = str(getattr(c, 'id', ''))
                c_cod = str(getattr(c, 'codigo', ''))
                if c_id == codigo or c_cod == codigo:
                    idx_remover = i
                    break

            if idx_remover is None:
                self.__tela_navio.mostra_erro('Carga não encontrada com este ID dentro deste navio.')
                continue # Pede o ID da carga ou do navio novamente (dependendo do fluxo desejado)

            # 7. Efetiva a remoção
            carga_removida = cargas.pop(idx_remover)
            
            # Atualiza lista no objeto e no DAO
            navio.cargas = list(cargas)
            self.__navio_DAO.update(navio)

            # Log
            self.__controlador_sistema.controlador_relatorio.registra_descarregamento(carga_removida)

            # Feedback e Atualização Visual
            self.__tela_navio.mostra_mensagem(f'Carga {getattr(carga_removida, "id", "")} removida com sucesso!')
            
            # Opcional: Mostra a lista de navios atualizada (que mostrará o navio com menos carga)
            self.lista()
            
            # Break para sair do loop while True após sucesso
            break

    def lista(self) -> bool:
        navios = self.__navio_DAO.get_all()
        
        if len(navios) == 0:
            sg.popup('Nenhum navio encontrado', title='Aviso')
            return False

        # --- CONSTRUÇÃO DO TEXTO DO RELATÓRIO ---
        texto_relatorio = ""
        
        for navio in navios:
            # 1. Extração de dados do Navio
            # (Mantendo a compatibilidade com dict ou objeto)
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

            # 2. Formatação do Cabeçalho do Navio
            texto_relatorio += "="*60 + "\n"
            texto_relatorio += f"🚢 NAVIO [{id_}]: {nome}\n"
            texto_relatorio += f"   Bandeira: {bandeira_txt} | Cia: {companhia_txt} | Cap: {capitao_txt}\n"
            texto_relatorio += "-"*60 + "\n"

            # 3. Detalhes das Cargas (Loop interno)
            if not cargas:
                texto_relatorio += "   [Sem cargas carregadas]\n"
            else:
                texto_relatorio += "   📦 CARGAS A BORDO:\n"
                for c in cargas:
                    # Extrai dados da Carga
                    cid = getattr(c, 'id', '')
                    cprod = getattr(c, 'produto', '')
                    ctipo = getattr(c, 'tipo', '')
                    cpeso = getattr(c, 'peso', 0)
                    cvalor = getattr(c, 'valor', 0)
                    
                    # Formata linha da carga
                    texto_relatorio += (f"   • ID: {cid} | Produto: {cprod} (Tipo {ctipo})\n"
                                        f"     Peso: {cpeso} kg | Valor: R$ {cvalor:.2f}\n")
                    texto_relatorio += "     " + "."*40 + "\n" # Separador leve entre cargas

            texto_relatorio += "\n" # Linha em branco entre navios

        # --- EXIBIÇÃO NA JANELA ---
        layout = [
            [sg.Text('Relatório Detalhado de Navios e Cargas', font=('Helvetica', 16))],
            [sg.Multiline(texto_relatorio, 
                          size=(80, 20),      # Largura, Altura (em caracteres)
                          font=('Courier', 10), # Fonte monoespaçada alinha melhor
                          disabled=True,      # Usuário não pode editar, só ler
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