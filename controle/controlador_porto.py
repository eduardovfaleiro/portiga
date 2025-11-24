from typing import Any
from controle.gerador_id import GeradorId
from models.cidade import Cidade
from models.porto import Porto
from telas.tela_porto import TelaPorto
from utils import Utils


class ControladorPorto(GeradorId, Utils):
    def __init__(self, controlador_sistema: Any):
        self.__portos: list[Porto] = []
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaPorto()

        super().__init__(self.__portos)
    
    def inclui(self):
        nome, cidade, pais, id_administrador = self.__tela.pega_dados().values()

        administrador = self.__controlador_sistema.controlador_admin.pega_por_id(id_administrador)

        porto = Porto(id=self.gera_id(), nome=nome, cidade=Cidade(cidade, pais), administrador=administrador)
        self.__portos.append(porto)
        self.__tela.mostra_mensagem('Porto adicionado com sucesso!')

    def abre_tela(self):
        opcoes: dict[int, Any] = {1: self.inclui, 2: self.exclui, \
                                  3: self.altera, 4: self.lista, 0: self.retorna}

        continua = True
        while continua:
            opcoes[self.__tela.abre_opcoes()]()

    def pega_porto_por_id(self, id: int):
        for i in range(len(self.__portos)):
            if self.__portos[i].id == id:
                return self.__portos[i]
            
        return None

    def lista(self) -> bool:
        # A mensagem de "Listando..." é implícita ao abrir a janela de listagem

        if len(self.__portos) == 0:
            # Em GUI, mostramos o erro/aviso em um popup
            self.__tela.mostra_erro('Nenhum porto encontrado')
            return False
        
        # Em vez de um loop de prints ou popups individuais,
        # passamos a lista completa para a tela montar a tabela.
        self.__tela.mostra_lista_portos(self.__portos)
        
        return True

    def exclui(self):
        self.__tela.mostra_titulo('Excluir Porto')

        tem_porto = self.lista()
        if not tem_porto: return

        while True:
            id = self.__tela.seleciona_id()
            if id == None: return

            for i in range(len(self.__portos)):
                porto = self.__portos[i]
                if porto.id == id:
                    self.__portos.pop(i)
                    self.__tela.mostra_mensagem(f'Porto {porto.id} excluída com sucesso!')
                    self.lista()
                    return
                    
            self.__tela.mostra_erro('Porto não existe')

    def altera(self):
        self.__tela.mostra_titulo('Alterar Porto')
        
        tem_portos = self.lista()
        if not tem_portos: return

        while True:
            id = self.__tela.seleciona_id()
            if id == None: return

            porto_atual = self.pega_porto_por_id(id)
            if porto_atual is None:
                self.__tela.mostra_erro('Porto não existe')
            else:
                break
        
        nome, cidade, pais, id_administrador = self.__tela.pega_dados_opcionais().values()
        
        if not self.valor_eh_vazio(nome):
            porto_atual.nome = nome

        if not self.valor_eh_vazio(cidade):
            porto_atual.cidade.nome = cidade

        if pais != None:
            porto_atual.cidade.pais = pais

        if id_administrador != None:
            administrador = self.__controlador_sistema.controlador_admin.pega_por_id(id_administrador)
            porto_atual.administrador = administrador

        self.__tela.mostra_mensagem(f'Porto {porto_atual.id} alterado com sucesso!')

    def retorna(self):
        self.__controlador_sistema.abre_tela()