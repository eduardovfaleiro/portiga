class Utils:
    def valor_eh_vazio(self, valor: str | None):
        return valor == None or valor.strip() == ''