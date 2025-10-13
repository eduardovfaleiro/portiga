from datetime import datetime

from models.navio import Navio

class Movimentacao:
    def __init__(self, id: int, navio: Navio, data_hora: datetime):
        self.__id = id
        self.__navio = navio
        self.__data_hora = data_hora

    @property
    def id(self):
        return self.__id

    @property
    def navio(self):
        return self.__navio
    
    @property
    def data_hora(self):
        return self.__data_hora
    
    
    def _data_hora_formatada(self, data_hora: datetime) -> str:
        return data_hora.strftime(r'%d/%m/%y %H:%M')

    def _set_length(self, string: str, length: int):
        if length < 4:
            raise Exception('length deve ser maior ou igual a 4')

        if len(string) < length:
            return string.rjust(length)

        str_cortada = string[:length-3]
        return f'{str_cortada}...'.rjust(length)