class No:
    pass


# Nó Operação Binária (+, -, *, etc)
class NoOperacao(No):
    """
    Construtor da classe.

    Recebe o tipo de operação e, opcionalmente, os filhos esquerdo e direito.
    Se os filhos esquerdo e direito não forem fornecidos na chamada ao construtor,
    inicializamos com valores padrão (None) só para criar os atributos.
    """

    def __init__(self, tipo: str, fesq=None, fdir=None):
        self.tipo = tipo
        self.fesq = fesq
        self.fdir = fdir

    def avalia(self):
        valor_esq = self.fesq.avalia()
        valor_dir = self.fdir.avalia()
        match self.tipo:
            case "+":
                return valor_esq + valor_dir
            case "-":
                return valor_esq - valor_dir
            case "*":
                return valor_esq * valor_dir
            case "/":
                return valor_esq / valor_dir
            case "//":
                return valor_esq // valor_dir
            case "print":
                print(valor_esq)
                return valor_esq


class NoNum(No):
    def __init__(self, valor: int | float):
        self.valor = valor

    def avalia(self) -> int | float:
        return self.valor
