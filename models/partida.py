from datetime import date, datetime
from models.movimentacao import Movimentacao
from models.navio import Navio
from models.porto import Porto

class Partida(Movimentacao):
    def __init__(self, id: int, navio: Navio, data_hora: datetime, destino: Porto):
        super().__init__(id, navio, data_hora)
        self.__destino = destino
    
    @property
    def destino(self):
        return self.__destino
    
    def to_string_resumido(self):
        max_length = 20
        # TODO(adicionar nome do navio e destino)
        return f"{self.id} {self._set_length('TESTE NOME NAVIO', max_length)} {self._data_hora_formatada(self.data_hora)} {self._set_length('TESTE NOME PORTO', max_length)}"
    
    def to_string_detalhado(self):
        return (
            f'Código: {self.id}\n'
            f'Navio: {self.navio}\n'
            f'Data e hora: {self._data_hora_formatada(self.data_hora)}\n'
            f'Destino (porto): {self.destino}\n'
        )