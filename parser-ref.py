from ply import lex, yacc

tokens = (
    "INT",
    "FLOAT",
    "MAIS",
    "MENOS",
    "DIVISAO",
    "MULTIPLICACAO",
    "DIVISAO_INTEIRA",
    "PRINT",
    "STRING",
    "PARENTESE_ABRE",
    "PARENTESE_FECHA",
)

t_INT = r"\d+"
t_FLOAT = r"\d+\.\d+"
t_MAIS = r"\+"
t_MENOS = r"\-"
t_DIVISAO = r"\/"
t_MULTIPLICACAO = r"\*"
t_DIVISAO_INTEIRA = r"\/\/"
t_PARENTESE_ABRE = r"\("
t_PARENTESE_FECHA = r"\)"
t_STRING = r'"[^\n"]*"|\'[^\n\']*\''  # significa procurar por aspas duplas ou simples, e dentro, qualquer coisa que não seja quebra de linha ou outras aspas.


def t_PRINT(
    token,
):  # a utilização de função aqui é que permite que a gente capte regex mais complexas, como as palvras reservadas.
    r"\bprint\b"
    return token


t_ignore = "\t \r\n"


def t_error(token):
    raise Exception("Recebi token inválido.")


# instanciamos o analisador léxico
analisador = lex.lex()

# --------------------------------------------

from arvore import *

# Regras de produção da gramática: funções começadas em "p_"


def p_expr_print(prod):
    """expr : PRINT PARENTESE_ABRE expr PARENTESE_FECHA"""
    prod[0] = NoOperacao(tipo="print")
    prod[0].fesq = prod[3]
    prod[0].fdir = None  # O nó de operação de print não tem filho direito


def p_expr_mais(prod):
    "expr : expr MAIS termo"
    prod[0] = NoOperacao(tipo="+")
    prod[0].fesq = prod[1]
    prod[0].fdir = prod[3]


def p_expr_menos(prod):
    "expr : expr MENOS termo"
    prod[0] = NoOperacao(tipo="-")
    prod[0].fesq = prod[1]
    prod[0].fdir = prod[3]


def p_expr_divisao(prod):
    "expr : expr DIVISAO termo"
    prod[0] = NoOperacao(tipo="/")
    prod[0].fesq = prod[1]
    prod[0].fdir = prod[3]


def p_expr_multiplicacao(prod):
    "expr : expr MULTIPLICACAO termo"
    prod[0] = NoOperacao(tipo="*")
    prod[0].fesq = prod[1]
    prod[0].fdir = prod[3]


def p_expr_divisao_inteira(prod):
    "expr : expr DIVISAO_INTEIRA termo"
    prod[0] = NoOperacao(
        tipo="//"
    )  # mesma operção das demais expressões, mas com o operador de divisão inteira
    prod[0].fesq = prod[1]
    prod[0].fdir = prod[3]


def p_expr_termo(prod):
    "expr : termo"
    prod[0] = prod[1]


def p_termo_fator(prod):
    "termo : fator"
    prod[0] = prod[1]


def p_fator_num(prod):
    """fator : INT
    | FLOAT"""
    if "." in prod[1]:
        prod[0] = NoNum(valor=float(prod[1]))
    else:
        prod[0] = NoNum(valor=int(prod[1]))


def p_termo_float(prod):
    "termo : FLOAT"
    prod[0] = NoNum(valor=float(prod[1]))


def p_termo_int(prod):
    "termo : INT"
    prod[0] = NoNum(valor=int(prod[1]))


def p_termo_string(prod):
    "termo : STRING"
    prod[0] = NoNum(valor=str(prod[1][1:-1]))


def p_termo_parentese(prod):
    "termo : PARENTESE_ABRE expr PARENTESE_FECHA"
    prod[0] = prod[2]


def p_error(produção):
    raise SyntaxError("Sintaxe inválida na nossa linguagem!")


parser = yacc.yacc(start="expr")

try:
    # Use 'utf-8-sig' para ignorar o caractere invisível de BOM do arquivo
    with open("prog.txt", "r", encoding="utf-8-sig") as f:
        entrada = f.read()

    if entrada.strip():
        analisador.input(entrada)
        resultado = parser.parse(entrada)
        if resultado is not None:
            print("Resultado:", resultado.avalia())
        else:
            print("Erro: A entrada não pôde ser analisada.")
    else:
        print("Arquivo vazio. Nada a processar.")
except FileNotFoundError:
    print("Arquivo 'prog.txt' não encontrado.")
except Exception as e:
    print(f"Erro: {e}")
