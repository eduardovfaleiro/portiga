from models.pessoa import Pessoa

class Administrador(Pessoa):
    def __init__(self, id: int, nome: str, telefone: int):
        super().__init__(id, nome)
        self.__telefone = telefone

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone: int):
        if not isinstance(telefone, int):
            raise TypeError("O telefone deve ser um int.")
        self.__telefone = telefone

        
    def __str__(self):
        return (
            f'Código: {self.id}\n'
            f'Nome: {self.nome}\n'
            f'Telefone: {self.telefone}'
        )