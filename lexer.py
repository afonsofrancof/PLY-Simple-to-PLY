from re import T
import ply.lex as lex

states = (
    ("lex", "exclusive"),
    ("yacc", "exclusive")
)

reserved = {
    "return": "RETURN",
    "error": "ERROR",
    "literals": "LITERALS",
    "ignore": "IGNORE",
    "tokens": "TOKENS",
    "precedence": "PRECEDENCE",
    "int": "INT",
    "float": "FLOAT"
}

tokens = ["LEX", "YACC", "PY", "RES", "TEXT",
          "STR", "COM", "EXP", "SNT", "ST", "LIT"] + list(reserved.values())

literals = ["[", "]", "(", ")", ",", "=", "%", ":"]
t_ANY_ignore = " \t\n\r"


def t_ANY_COM(t):
    r"[#].*\n"
    pass


def t_LEX(t):
    r"%%\s?LEX"
    t.lexer.push_state("lex")
    pass


def t_lex_yacc_STR(t):
    r"[fr]?(\"[^\"]*\"|\'[^']*\')"
    return t


def t_lex_RES(t):
    r"t(\.\w+)+(\(\d*\))?"
    return t


def t_lex_YACC(t):
    r"%%\s?YACC"
    t.lexer.pop_state()
    print("------------------------------------------------")
    t.lexer.push_state("yacc")
    pass


# # r"[a-z]+\ :\ ([^\{]|\'\{\'|\"\{\")+ "
# def t_yacc_EXP(t):
#     r"[a-z]+\ :\ ([^\{]|\'\{\'|\"\{\")+(\w|\')"
#     return t


def t_yacc_SNT(t):
    r"[a-z]+"
    return t


def t_yacc_ST(t):
    r"[A-Z]+"
    return t

def t_yacc_LIT(t):
    r"\'.+\'"
    return t


def t_lex_yacc_TEXT(t):
    r"\w+"
    t.type = reserved.get(t.value, "TEXT")
    return t


def t_yacc_RES(t):
    r"{.*}"
    return t


def t_yacc_PY(t):
    r"%%"
    t.lexer.pop_state()
    pass


def t_PY(t):
    r"(.|\n)+"
    return t


def t_ANY_error(t):
    print("Illegal Character: ", t.value[0])


lexer = lex.lex()
f = open('exemplo.in', 'r')
text = f.read()
lexer.input(text)

for tok in lexer:
    print(tok)

f.close()
