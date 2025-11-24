from typing import Any
from entidade.relatorio import Relatorio
from tela.tela_relatorio import TelaRelatorio
from entidade.carga import Carga 

class ControladorRelatorio:
    def __init__(self, controlador_sistema: Any):
        self.__relatorio = Relatorio()
        self.__tela = TelaRelatorio()
        self.__controlador_sistema = controlador_sistema

    def traduz_estatisticas(self, estatisticas: dict) -> dict:
        estatisticas_traduzidas = {}
        mapa_tipos = Carga.tipos_carga

        for chave in ['carregamentos', 'descarregamentos']:
            traduzidos = {}
            for codigo, qtd in estatisticas.get(chave, {}).items():

                key = int(codigo) if str(codigo).isdigit() else codigo
                
                nome = mapa_tipos.get(key, f"Tipo {codigo} desconhecido")
                traduzidos[nome] = qtd
            estatisticas_traduzidas[chave] = traduzidos
            
        return estatisticas_traduzidas

    def registra_carregamento(self, carga):
        self.__relatorio.registra_carregamento(carga)

    def registra_descarregamento(self, carga):
        self.__relatorio.registra_descarregamento(carga)

    def mostra_relatorio(self):
        estatisticas = self.__relatorio.get_estatisticas()
        
        estatisticas_traduzidas = self.traduz_estatisticas(estatisticas)
        
        self.__tela.mostra_relatorio(estatisticas_traduzidas)

    def abre_tela(self):
        self.mostra_relatorio()