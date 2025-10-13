from datetime import date, datetime
from models.movimentacao import Movimentacao
from models.navio import Navio
from models.porto import Porto

class Chegada(Movimentacao):
    def __init__(self, id: int, navio: Navio, data_hora: datetime, dias_viagem: int, procedencia: Porto):
        self.__id = id
        super().__init__(id, navio, data_hora)
        self.__dias_viagem = dias_viagem
        self.__procedencia = procedencia
        
    @property
    def dias_viagem(self):
        return self.__dias_viagem
    
    @property
    def procedencia(self):
        return self.__procedencia
   
    def to_string_resumido(self):
        max_length = 20
        # TODO(adicionar nome do navio e procedencia)
        return f'{self.id} {self._set_length('TESTE NOME NAVIO', max_length)} {self._data_hora_formatada(self.data_hora)} {self._set_length('TESTE NOME PORTO', max_length)}'

    def to_string_detalhado(self):
        return (
            f'Código: {self.id}\n'
            f'Navio: {self.navio}\n'
            f'Data e hora: {self._data_hora_formatada(self.data_hora)}\n'
            f'Procedência (porto): {self.procedencia}\n'
            f'Dias de viagem: {self.dias_viagem}'
        )