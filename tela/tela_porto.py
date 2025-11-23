from typing import Any
from tela.seletor_pais import SeletorPais
from tela.tela_utils import TelaUtils


class TelaPorto(TelaUtils, SeletorPais):
    __opcoes = {1: 'Incluir', 2: 'Excluir', 3: 'Alterar', 4: 'Listar', 0: 'Retornar'}

    def pega_dados(self) -> dict[str, Any]:
        self.mostra_titulo('Dados Porto')
        
        while True:
            nome = input("Nome: ")
            if self.valor_eh_vazio(nome):
                self.mostra_erro('Nome do porto não pode ser vazio')
            else:
                break

        while True:
            cidade = input("Cidade: ")
            if self.valor_eh_vazio(cidade):
                self.mostra_erro('Nome da cidade não pode ser vazio')
            else:
                break

        while True:
            codigo_pais = input("País (código ISO 3166): ")
            pais = self.retorna_pais(codigo_pais)

            if pais is not None:
                break

            self.mostra_erro('Código de país no padrão ISO 3166 não existe')

        return {'nome': nome, 'cidade': cidade, 'pais': pais}
    

    def pega_dados_opcionais(self) -> dict[str, Any]:
        self.mostra_titulo('Novos Dados Porto')

        nome = input("Nome: ")
        if self.valor_eh_vazio(nome):
            nome = None

        cidade = input("Cidade: ")
        if self.valor_eh_vazio(cidade):
            cidade = None

        while True:
            codigo_pais_sede = input("País (código ISO 3166): ")
            if self.valor_eh_vazio(codigo_pais_sede):
                pais = None
                break

            pais = self.retorna_pais(codigo_pais_sede)

            if pais is not None:
                break

            self.mostra_erro('Código de país no padrão ISO 3166 não existe')

        return {"nome": nome, "cidade": cidade, "pais": pais, "administrador": None}

    def abre_opcoes(self):
        self.mostra_titulo('Portos')
        self.mostra_opcoes(self.__opcoes)
        return self.recebe_opcao(self.__opcoes)