from lib2to3.pgen2 import literals
import ply.lex as lex

states = (
    ("lex","exclusive"),
    ("yacc","exclusive")
)

reserved = {
    "return": "RETURN",
    "error": "ERROR"
}

tokens = ["TEXT","LEX","YACC","VAL"] + list(reserved.values())

literals = ["[","]","(",")",",","="]

ignore = " \t\n\r"

t_RET = r"return"



t_TEXT = r""

def t_error(t):
    print("Illegal Character: ", t.value[0])


lexer = lex.lex()