import json
from typing import Any
from models.companhia import Companhia
from models.pais import Pais
from telas.tela_utils import TelaUtils
import re


class TelaCompanhia(TelaUtils):
    __opcoes = {1: 'Incluir', 2: 'Excluir', 3: 'Alterar', 4: 'Listar', 0: 'Retornar'}

    def abre_opcoes(self):
        self.mostra_titulo('Companhias')
        self.mostra_opcoes(self.__opcoes)
        return self.recebe_opcao(self.__opcoes)

    def pega_dados_companhia(self) -> dict[str, Any]:
        self.mostra_titulo('Dados Companhia')
        
        while True:
            nome = input("Nome: ")
            if nome.strip() == '':
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

        if nome.strip() == '':
            nome = None

        while True:
            codigo_pais_sede = input("País sede (código ISO 3166): ")
            if codigo_pais_sede.strip() == '':
                pais = None
                break

            pais = self.retorna_pais(codigo_pais_sede)

            if pais is not None:
                break

            self.mostra_erro('Código de país no padrão ISO 3166 não existe')

        return {"nome": nome, "pais_sede": pais}
    
    # TODO(Corrigir)
    def retorna_pais(self, codigo_pais: str) -> Pais | None:
        paises: dict[str, str] = {}
        with open('countries.json', 'r', encoding='utf-8') as paises_json:
            paises_dict = json.load(paises_json)

            for pais_item in paises_dict:
                paises[pais_item.get('code')] = pais_item.get('name')

        pais_nome = paises.get(codigo_pais)

        if pais_nome is not None:
            return Pais(codigo=codigo_pais, nome=pais_nome)
        else:
            return None

    def mostra_companhia(self, companhia: Companhia):
        print(f'Código: {companhia.id}')
        print(f'Nome: {companhia.nome}')
        print(f'País sede: {companhia.pais_sede.codigo} {companhia.pais_sede.nome}\n')

    def seleciona_companhia(self) -> int:
        pattern = r'^\d+$'

        while True:
            user_input = input("Código da companhia que deseja selecionar (\"sair\" para cancelar): ")
            has_only_digits = re.match(pattern, user_input) != None
            if has_only_digits:
                break
            else:
                self.mostra_erro('Código da companhia só pode ser composto por dígitos')

        id = int(user_input)
        return id
    
    def mostra_mensagem(self, mensagem: str):
        print(mensagem)