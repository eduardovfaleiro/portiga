
import re


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

    def valor_eh_vazio(self, valor: str):
        return valor.strip() == ''
    
    def mostra_mensagem(self, mensagem: str):
        print(mensagem)

    def seleciona_id(self) -> int | None:
        pattern = r'^\d+$'

        while True:
            user_input = input("Código que deseja selecionar (\"sair\" para cancelar): ")
            if user_input == 'sair':
                return None

            has_only_digits = re.match(pattern, user_input) != None
            if has_only_digits:
                break
            else:
                self.mostra_erro('Código só pode ser composto por dígitos')

        id = int(user_input)
        return id