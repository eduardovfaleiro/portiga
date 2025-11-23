from entidade.carga import Carga
from tela.tela_utils import TelaUtils

class TelaRelatorio(TelaUtils):
    def mostra_relatorio(self, estatisticas: dict):
        self.mostra_titulo('Relatórios')
        print("Carregamentos:")
        for categoria, qtd in estatisticas['carregamentos'].items():
            nome_categoria = Carga.tipos_carga.get(categoria, "Tipo desconhecido")
            print(f"- {nome_categoria}: {qtd}")

        print("\nDescarregamentos:")
        for categoria, qtd in estatisticas['descarregamentos'].items():
            nome_categoria = Carga.tipos_carga.get(categoria, "Tipo desconhecido")
            print(f"- {nome_categoria}: {qtd}")