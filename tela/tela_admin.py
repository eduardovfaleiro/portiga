from typing import Any
from tela.tela_utils import TelaUtils

class TelaAdmin(TelaUtils):
    __opcoes = {1: 'Incluir', 2: 'Excluir', 3: 'Listar', 0: 'Retornar'}

    def abre_opcoes(self) -> int:
        self.mostra_titulo('Administradores')
        self.mostra_opcoes(self.__opcoes)
        return self.recebe_opcao(self.__opcoes)

    def pega_dados(self) -> dict[str, Any]:
        self.mostra_titulo('Dados Administrador')
        nome = self.pega_str('Nome: ', 'Nome não pode ser vazio')
        telefone = self.pega_digito('Telefone: ', 'Telefone só pode conter dígitos')
        return {'nome': nome, 'telefone': telefone}