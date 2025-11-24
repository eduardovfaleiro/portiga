from datetime import date, datetime
from entidade.movimentacao import Movimentacao
from entidade.navio import Navio
from entidade.porto import Porto

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
        na_str = self._set_length('N/A', max_length)
        navio_nome = self._set_length(self.navio.nome, max_length) if self.navio != None else na_str
        procedencia_nome = self._set_length(self.procedencia.nome, max_length) if self.procedencia != None else na_str
        return f"{self.id} {navio_nome} {self._data_hora_formatada(self.data_hora)} {procedencia_nome} {self.dias_viagem}"


    def to_string_detalhado(self):
        navio = self.navio if self.navio != None else 'N/A'
        procedencia = f'{self.procedencia.id} {self.procedencia.nome}' if self.procedencia != None else 'N/A'

        return (
            f'Código: {self.id}\n'
            f'Navio: {navio}\n'
            f'Data e hora: {self._data_hora_formatada(self.data_hora)}\n'
            f'Procedência (porto): {procedencia}\n'
            f'Dias de viagem: {self.dias_viagem}'
        )