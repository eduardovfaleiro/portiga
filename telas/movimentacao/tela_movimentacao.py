from datetime import datetime
from models.navio import Navio
from telas.tela_utils import TelaUtils


class TelaMovimentacao(TelaUtils):
    def pega_digito(self, mensagem_input: str, mensagem_erro: str) -> int:
        while True:
            digito_str = input(mensagem_input)
            if digito_str.isdigit():
                return int(digito_str)
                
            self.mostra_erro('Código do navio só pode ser composto por dígitos')

    def pega_data_hora(self) -> datetime:
        while True:
            data_hora = input("Data e hora (padrão: agora | formato: dd/MM/yy hh:mm): ")
            if self.valor_eh_vazio(data_hora):
                return datetime.now()

            try:
                return datetime.strptime(data_hora, r'%d/%m/%y %H:%M')
            except:
                self.mostra_erro('Data e hora inválidos. Utilize o formato dd/MM/yy hh:mm.')