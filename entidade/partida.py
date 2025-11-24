from datetime import date, datetime
from entidade.movimentacao import Movimentacao
from entidade.navio import Navio
from entidade.porto import Porto

class Partida(Movimentacao):
    def __init__(self, id: int, navio: Navio, data_hora: datetime, destino: Porto):
        super().__init__(id, navio, data_hora)
        self.__destino = destino
    
    @property
    def destino(self):
        return self.__destino

    def to_string_resumido(self):
        max_length = 20
        na_str = self._set_length('N/A', max_length)
        navio_nome = self._set_length(self.navio.nome, max_length) if self.navio != None else na_str
        destino_nome = self._set_length(self.destino.nome, max_length) if self.destino != None else na_str
        return f"{self.id} {navio_nome} {self._data_hora_formatada(self.data_hora)} {destino_nome}"
    
    def to_string_detalhado(self):
        navio = self.navio if self.navio != None else 'N/A'
        destino = f'{self.destino.id} {self.destino.nome}' if self.destino != None else 'N/A'

        return (
            f'Código: {self.id}\n'
            f'Navio: {navio}\n'
            f'Data e hora: {self._data_hora_formatada(self.data_hora)}\n'
            f'Destino (porto): {destino}'
        )