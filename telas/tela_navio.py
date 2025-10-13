import json
import os
import re
from typing import Any
from models.pais import Pais
from telas.seletor_pais import SeletorPais
from telas.tela_utils import TelaUtils


class TelaNavio(TelaUtils, SeletorPais):
    __opcoes = {1: 'Incluir', 2: 'Excluir', 3: 'Alterar', 4: 'Listar', 5: 'Carregar', 6: 'Descarregar', 0: 'Retornar'}
 
    def abre_opcoes(self) -> int:
        self.mostra_titulo('Navios')
        self.mostra_opcoes(self.__opcoes)
        return self.recebe_opcao(self.__opcoes)

    def pega_dados_navio(self) -> dict[str, Any]:
        self.mostra_titulo('Dados Navio')

        while True:
            nome = input("Nome: ").strip()
            if self.valor_eh_vazio(nome):
                self.mostra_erro('Nome do navio não pode ser vazio')
            else:
                break

        while True:
            codigo_bandeira = input("Bandeira (código ISO 3166): ").strip().upper()
            bandeira = self.retorna_pais(codigo_bandeira)
            if bandeira is not None:
                break
            self.mostra_erro('Código de país no padrão ISO 3166 não existe')

        # Companhia (id)
        while True:
            companhia_raw = input("Código da companhia (dígitos): ").strip()
            if companhia_raw.isdigit():
                companhia_id = int(companhia_raw)
                break
            self.mostra_erro('Código da companhia só pode ser composto por dígitos')

        # Capitão (id)
        while True:
            capitao_raw = input("Código do capitão (dígitos): ").strip()
            if capitao_raw.isdigit():
                capitao_id = int(capitao_raw)
                break
            self.mostra_erro('Código do capitão só pode ser composto por dígitos')

        return {
            "nome": nome,
            "bandeira": bandeira,
            "companhia": companhia_id,
            "capitao": capitao_id,
        }

    def pega_dados_opcionais_navio(self) -> dict[str, Any]:
        self.mostra_titulo('Novos Dados Navio')

        nome = input("Nome: ").strip()
        if nome == '':
            nome = None

        # Bandeira opcional
        while True:
            codigo_bandeira = input("Bandeira (código ISO 3166): ").strip().upper()
            if codigo_bandeira == '':
                bandeira = None
                break
            bandeira = self.retorna_bandeira(codigo_bandeira)
            if bandeira is not None:
                break
            self.mostra_erro('Código de país no padrão ISO 3166 não existe')

        # Companhia opcional
        while True:
            companhia_raw = input("Código da companhia: ").strip()
            if companhia_raw == '':
                companhia = None
                break
            if companhia_raw.isdigit():
                companhia = int(companhia_raw)
                break
            self.mostra_erro('Código da companhia só pode ser composto por dígitos')

        # Capitão opcional
        while True:
            capitao_raw = input("Código do capitão: ").strip()
            if capitao_raw == '':
                capitao = None
                break
            if capitao_raw.isdigit():
                capitao = int(capitao_raw)
                break
            self.mostra_erro('Código do capitão só pode ser composto por dígitos')

        return {
            "nome": nome,
            "bandeira": bandeira,
            "companhia": companhia,
            "capitao": capitao,
        }

    def pega_dados_carga(self) -> dict[str, Any] | None:
        """Solicita tipo, peso e valor da carga e retorna um dicionário ou None."""
        self.mostra_titulo('Dados da Carga')

        tipo = input('Tipo da carga: ').strip()
        if tipo == '':
            self.mostra_erro('Tipo não pode ser vazio.')
            return None

        peso_raw = input('Peso (kg): ').strip()
        try:
            peso = float(peso_raw)
            if peso < 0:
                raise ValueError()
        except Exception:
            self.mostra_erro('Peso inválido.')
            return None

        valor_raw = input('Valor (R$): ').strip()
        try:
            valor = float(valor_raw)
            if valor < 0:
                raise ValueError()
        except Exception:
            self.mostra_erro('Valor inválido.')
            return None

        return {'tipo': tipo, 'peso': peso, 'valor': valor}

    def seleciona_carga(self) -> str | None:
        """Pede ao usuário o código/id da carga (string sem espaços) para selecionar/descarregar."""
        pattern = r'^\S+$'
        while True:
            user_input = input('Código da carga ("sair" para cancelar): ').strip()
            if user_input.lower() == 'sair' or user_input == '':
                return None
            if re.match(pattern, user_input):
                return user_input
            self.mostra_erro('Código da carga inválido (não pode conter espaços).')

    def retorna_bandeira(self, codigo_bandeira: str) -> Pais | None:
        if codigo_bandeira == '':
            return None
        bandeira_nome = self.__paises.get(codigo_bandeira)
        if bandeira_nome is not None:
            return Pais(codigo=codigo_bandeira, nome=bandeira_nome)
        return None

    def mostra_navio(self, navio: Any):
        # aceita objeto com atributos ou dict
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

        bandeira_txt = f'{bandeira.codigo} {bandeira.nome}' if bandeira else 'N/A'
        companhia_txt = f'{companhia.id} {companhia.nome}' if companhia else 'N/A'
        capitao_txt = f'{capitao.id} {capitao.nome}' if capitao else 'N/A'

        print(f'Código: {id_}')
        print(f'Nome: {nome}')
        print(f'Bandeira: {bandeira_txt}')
        print(f'Companhia: {companhia_txt}')
        print(f'Capitão: {capitao_txt}')

        # mostra resumo das cargas embarcadas (se houver)
        if cargas:
            if isinstance(cargas, list):
                cargas_txt = []
                for c in cargas:
                    cid = getattr(c, 'id', None) or getattr(c, 'codigo', None) or str(c)
                    ctipo = getattr(c, 'tipo', '') or ''
                    cpeso = getattr(c, 'peso', '') or ''
                    cvalor = getattr(c, 'valor', '') or ''
                    cargas_txt.append(f'{cid}: {ctipo}, {cpeso} kg, R${cvalor}')
                print('Cargas:', ' | '.join(cargas_txt))
            else:
                print('Cargas: N/A')
        else:
            print('Cargas: Nenhuma')

    def seleciona_navio(self) -> int | None:
        pattern = r'^\d+$'
        while True:
            user_input = input('Código do navio que deseja selecionar ("sair" para cancelar): ').strip()
            if user_input.lower() == 'sair' or user_input == '':
                return None
            if re.match(pattern, user_input):
                return int(user_input)
            self.mostra_erro('Código do navio só pode ser composto por dígitos')

    def mostra_mensagem(self, mensagem: str):
        print(mensagem)