

from tela.tela_utils import TelaUtils


class TelaSistema(TelaUtils):
    __opcoes = {1: 'Companhias', 2: 'Navios', 3: 'Portos', 4: 'Chegadas', 5: 'Partidas', 6: 'Capitães', 7: 'Relatórios', 8: 'Administradores', 0: 'Finalizar sistema'}
    
    def abre_opcoes(self) -> int:
        self.mostra_titulo('Portiga')
        self.mostra_opcoes(self.__opcoes)
        return self.recebe_opcao(self.__opcoes)
