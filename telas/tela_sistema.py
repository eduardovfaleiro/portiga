

from telas.tela_utils import TelaUtils


class TelaSistema(TelaUtils):
    __opcoes = {2: 'Companhias', 1: 'Navios', 0: 'Finalizar sistema'}
    
    def abre_opcoes(self) -> int:
        self.mostra_titulo('Portiga')
        self.mostra_opcoes(self.__opcoes)
        return self.recebe_opcao(self.__opcoes)
