from collections import Counter
from entidade.carga import Carga

class Relatorio:
    def __init__(self):
        # separate counters
        self.__carregamentos = Counter()
        self.__descarregamentos = Counter()

    def registra_carregamento(self, carga: Carga):
        categoria = getattr(carga, 'tipo', 'Desconhecido')
        self.__carregamentos[categoria] += 1

    def registra_descarregamento(self, carga: Carga):
        categoria = getattr(carga, 'tipo', 'Desconhecido')
        self.__descarregamentos[categoria] += 1

    def get_estatisticas(self) -> dict:
        return {
            'carregamentos': dict(self.__carregamentos),
            'descarregamentos': dict(self.__descarregamentos)
        }