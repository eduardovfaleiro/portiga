from entidade.carga import Carga
from tela.tela_utils import TelaUtils
import FreeSimpleGUI as sg

class TelaRelatorio(TelaUtils):
    def mostra_relatorio(self, estatisticas: dict):
        # 1. Montagem do Cabeçalho e do Título da Janela
        texto_relatorio = "=== RELATÓRIO DE MOVIMENTAÇÃO DE CARGAS ===\n\n"
        
        # 2. Processamento dos Carregamentos
        texto_relatorio += "CARREGAMENTOS:\n"
        carregamentos = estatisticas.get('carregamentos', {})
        
        if not carregamentos:
            texto_relatorio += "  Nenhum carregamento registrado.\n"
        else:
            for categoria, qtd in carregamentos.items():
                # O Carga.tipos_carga deve ser acessível aqui (ou importado/passado)
                nome_categoria = Carga.tipos_carga.get(categoria, f"Tipo {categoria} desconhecido")
                texto_relatorio += f"  - {nome_categoria}: {qtd}\n"

        # 3. Processamento dos Descarregamentos
        texto_relatorio += "\nDESCARREGAMENTOS:\n"
        descarregamentos = estatisticas.get('descarregamentos', {})
        
        if not descarregamentos:
            texto_relatorio += "  Nenhum descarregamento registrado.\n"
        else:
            for categoria, qtd in descarregamentos.items():
                nome_categoria = Carga.tipos_carga.get(categoria, f"Tipo {categoria} desconhecido")
                texto_relatorio += f"  - {nome_categoria}: {qtd}\n"

        # 4. Exibição na Janela GUI
        layout = [
            [sg.Text('Relatório de Cargas', font=('Helvetica', 18))],
            # Multiline é ideal para relatórios com muitas linhas e rolagem
            [sg.Multiline(default_text=texto_relatorio, 
                          size=(60, 15), 
                          font=('Courier', 10), # Fonte monoespaçada para alinhamento perfeito
                          disabled=True, 
                          autoscroll=True)],
            [sg.Button('Fechar', size=(10, 1))]
        ]

        window = sg.Window('Relatórios de Movimentação', layout)
        window.read()
        window.close()