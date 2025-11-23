from datetime import datetime
from entidade.navio import Navio
from tela.tela_utils import TelaUtils


class TelaMovimentacao(TelaUtils):
    def pega_data_hora(self) -> datetime:
        while True:
            data_hora = input("Data e hora (padrão: agora | formato: dd/MM/yy hh:mm): ")
            if self.valor_eh_vazio(data_hora):
                return datetime.now()

            try:
                return datetime.strptime(data_hora, r'%d/%m/%y %H:%M')
            except:
                self.mostra_erro('Data e hora inválidos. Utilize o formato dd/MM/yy hh:mm.')