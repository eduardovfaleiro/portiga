import re
from typing import Any
from telas.tela_utils import TelaUtils

class TelaCapitao(TelaUtils):
    __opcoes = {1: 'Incluir', 2: 'Excluir', 3: 'Listar', 0: 'Retornar'}

    def abre_opcoes(self) -> int:
        self.mostra_titulo('Capitães')
        self.mostra_opcoes(self.__opcoes)
        return self.recebe_opcao(self.__opcoes)

    def pega_dados_capitao(self) -> dict[str, Any]:
        self.mostra_titulo('Dados Capitão')
        while True:
            nome = input('Nome: ').strip()
            if nome == '':
                self.mostra_erro('Nome não pode ser vazio')
            else:
                break
        return {'nome': nome}

    def mostra_capitao(self, capitao: Any, indice: int | None = None):
        prefix = f'[{indice}] ' if indice is not None else ''
        nome = getattr(capitao, 'nome', str(capitao))
        print(f'{prefix}Nome: {nome}')

    def seleciona_capitao(self) -> int | None:
        pattern = r'^\d+$'
        while True:
            user_input = input('Índice do capitão ("sair" para cancelar): ').strip()
            if user_input.lower() == 'sair' or user_input == '':
                return None
            if re.match(pattern, user_input):
                return int(user_input)
            self.mostra_erro('Índice inválido. Informe apenas dígitos.')

    def mostra_titulo(self, texto: str) -> None:
        print(f'\n=== {texto} ===')

    def mostra_mensagem(self, mensagem: str) -> None:
        print(mensagem)

    def mostra_erro(self, mensagem: str) -> None:
        print(f'ERRO: {mensagem}')