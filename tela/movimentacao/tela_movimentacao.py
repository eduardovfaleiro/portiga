from datetime import datetime
from entidade.navio import Navio
from tela.tela_utils import TelaUtils


import FreeSimpleGUI as sg

class TelaMovimentacao(TelaUtils):
    def valida_converte_data(self, data_str: str) -> datetime | None:
        if not data_str or data_str.strip() == '':
            return datetime.now()
        
        try:
            return datetime.strptime(data_str, r'%d/%m/%y %H:%M')
        except ValueError:
            return None