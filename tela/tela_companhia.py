
from typing import Any
from entidade.companhia import Companhia
from tela.seletor_pais import SeletorPais
from tela.tela_utils import TelaUtils

class TelaCompanhia(TelaUtils, SeletorPais):
    __opcoes = {1: 'Incluir', 2: 'Excluir', 3: 'Alterar', 4: 'Listar', 0: 'Retornar'}

    def abre_opcoes(self):
        self.mostra_titulo('Companhias')
        self.mostra_opcoes(self.__opcoes)
        return self.recebe_opcao(self.__opcoes)

    def pega_dados_companhia(self) -> dict[str, Any]:
        self.mostra_titulo('Dados Companhia')
        
        while True:
            nome = input("Nome: ")
            if self.valor_eh_vazio(nome):
                self.mostra_erro('Nome da companhia não pode ser vazio')
            else:
                break
                
        while True:
            codigo_pais_sede = input("País sede (código ISO 3166): ")
            pais = self.retorna_pais(codigo_pais_sede)

            if pais is not None:
                break

            self.mostra_erro('Código de país no padrão ISO 3166 não existe')

        return {"nome": nome, "pais_sede": pais}
    
    def pega_dados_opcionais_companhia(self) -> dict[str, Any]:
        self.mostra_titulo('Novos Dados Companhia')
        nome = input("Nome: ")

        if self.valor_eh_vazio(nome):
            nome = None

        while True:
            codigo_pais_sede = input("País sede (código ISO 3166): ")
            if self.valor_eh_vazio(codigo_pais_sede):
                pais = None
                break

            pais = self.retorna_pais(codigo_pais_sede)

            if pais is not None:
                break

            self.mostra_erro('Código de país no padrão ISO 3166 não existe')

        return {"nome": nome, "pais_sede": pais}