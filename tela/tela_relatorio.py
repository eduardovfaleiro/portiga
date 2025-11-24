from tela.tela_utils import TelaUtils
import FreeSimpleGUI as sg

class TelaRelatorio(TelaUtils):
    def mostra_relatorio(self, estatisticas: dict):
        texto_relatorio = "=== RELATÓRIO DE MOVIMENTAÇÃO DE CARGAS ===\n\n"
        
        texto_relatorio += "CARREGAMENTOS:\n"
        carregamentos = estatisticas.get('carregamentos', {})
        
        if not carregamentos:
            texto_relatorio += "  Nenhum carregamento registrado.\n"
        else:
            for nome_categoria, qtd in carregamentos.items(): 
                texto_relatorio += f"  - {nome_categoria}: {qtd}\n"

        texto_relatorio += "\nDESCARREGAMENTOS:\n"
        descarregamentos = estatisticas.get('descarregamentos', {})
        
        if not descarregamentos:
            texto_relatorio += "  Nenhum descarregamento registrado.\n"
        else:
            for nome_categoria, qtd in descarregamentos.items():
                texto_relatorio += f"  - {nome_categoria}: {qtd}\n"

        layout = [
            [sg.Text('Relatório de Cargas', font=('Helvetica', 18))],
            [sg.Multiline(default_text=texto_relatorio, 
                          size=(60, 15), 
                          font=('Courier', 10), 
                          disabled=True, 
                          autoscroll=True)],
            [sg.Button('Fechar', size=(10, 1))]
        ]

        window = sg.Window('Relatórios de Movimentação', layout)
        window.read()
        window.close()