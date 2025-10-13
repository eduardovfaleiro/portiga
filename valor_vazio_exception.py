class ValorVazioException(Exception):
    def __init__(self, mensagem: str="O valor não pode ser vazio."):
        super().__init__(mensagem)