import re
from typing import Any
from tela.tela_utils import TelaUtils


class TelaCarga(TelaUtils):
    __opcoes = {1: 'Incluir', 2: 'Excluir', 3: 'Listar', 0: 'Retornar'}

    def abre_opcoes(self) -> int:
        self.mostra_titulo('Cargas')
        self.mostra_opcoes(self.__opcoes)
        return self.recebe_opcao(self.__opcoes)

    def pega_dados_carga(self) -> dict[str, Any] | None:
        self.mostra_titulo('Dados Carga')

        id = input('Código: ').strip()
        if id == '':
            self.mostra_erro('Código não pode ser vazio')
            return None

        produto = input('Produto: ').strip()
        if produto == '':
            self.mostra_erro('Produto não pode ser vazio')
            return None

        tipo_raw = input('Tipo: ').strip()
        tipo = int(tipo_raw)
        if tipo == '':
            self.mostra_erro('Tipo não pode ser vazio')
            return None
        if tipo < 1 or tipo > 4:
            self.mostra_erro('Tipo deve ser um número entre 1 e 4')
            return None

        peso_raw = input('Peso (kg): ').strip()
        try:
            peso = float(peso_raw)
            if peso < 0:
                raise ValueError()
        except Exception:
            self.mostra_erro('Peso inválido')
            return None

        valor_raw = input('Valor (R$): ').strip()
        try:
            valor = float(valor_raw)
            if valor < 0:
                raise ValueError()
        except Exception:
            self.mostra_erro('Valor inválido')
            return None

        return {'id': id, 'produto': produto, 'tipo': tipo, 'peso': peso, 'valor': valor}

    def mostra_carga(self, carga: Any):
        id = getattr(carga, 'id', '')
        produto = getattr(carga, 'produto', '')
        tipo = getattr(carga, 'tipo', '')
        peso = getattr(carga, 'peso', '')
        valor = getattr(carga, 'valor', '')
        print(f'Código: {id} | Produto: {produto} | Tipo: {tipo} | Peso: {peso} kg | Valor: R$ {valor}')

    def seleciona_carga(self) -> str | None:
        pattern = r'^\S+$'  # código sem espaços
        while True:
            user_input = input('Código da carga ("sair" para cancelar): ').strip()
            if user_input.lower() == 'sair' or user_input == '':
                return None
            if re.match(pattern, user_input):
                return user_input
            self.mostra_erro('Código inválido')

    def mostra_titulo(self, texto: str) -> None:
        print(f'\n=== {texto} ===')

    def mostra_mensagem(self, mensagem: str) -> None:
        print(mensagem)

    def mostra_erro(self, mensagem: str) -> None:
        print(f'ERRO: {mensagem}')