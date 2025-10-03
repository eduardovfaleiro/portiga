from typing import Any, Callable, TypeVar


class TelaUtils:
    def mostra_erro(self, mensagem: str):
        print(f'ERRO: {mensagem}')

    def mostra_titulo(self, titulo: str):
        LARGURA_TOTAL = 50
        conteudo = f" {titulo} " 
        espaco_preencher = LARGURA_TOTAL - len(conteudo)
        hifens_lado = espaco_preencher // 2
        string_hifens = "-" * hifens_lado
        
        resultado = string_hifens + conteudo + string_hifens
        
        if len(resultado) < LARGURA_TOTAL:
            resultado += "-"
            
        print(resultado)

    def mostra_opcoes(self, opcoes: dict[int, str]):
        for num_opcao, opcao in opcoes.items():
            print(f'{num_opcao} - {opcao}')

    def recebe_opcao(self, opcoes: dict[int, str],
                     mensagem_input: str = 'Escolha a opção: ',
                     erro_mensagem: str = 'Opção não existe'):
        while True:
            opcao = input(mensagem_input)

            if opcao in map(str, list(opcoes.keys())):
                return int(opcao)
            else:
                self.mostra_erro(erro_mensagem)