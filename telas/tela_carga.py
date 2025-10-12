import re
from typing import Any
from telas.tela_utils import TelaUtils


class TelaCarga(TelaUtils):
    __opcoes = {1: 'Incluir', 2: 'Excluir', 3: 'Listar', 0: 'Retornar'}

    def abre_opcoes(self) -> int:
        self.mostra_titulo('Cargas')
        self.mostra_opcoes(self.__opcoes)
        return self.recebe_opcao(self.__opcoes)

    def pega_dados_carga(self) -> dict[str, Any] | None:
        self.mostra_titulo('Dados Carga')

        codigo = input('Código: ').strip()
        if codigo == '':
            self.mostra_erro('Código não pode ser vazio')
            return None

        tipo = input('Tipo: ').strip()
        if tipo == '':
            self.mostra_erro('Tipo não pode ser vazio')
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

        return {'codigo': codigo, 'tipo': tipo, 'peso': peso, 'valor': valor}

    def mostra_carga(self, carga: Any):
        codigo = getattr(carga, 'codigo', '')
        tipo = getattr(carga, 'tipo', '')
        peso = getattr(carga, 'peso', '')
        valor = getattr(carga, 'valor', '')
        print(f'Código: {codigo} | Tipo: {tipo} | Peso: {peso} kg | Valor: R$ {valor}')

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