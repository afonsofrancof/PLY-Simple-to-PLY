from re import T
import ply.lex as lex

states = (
    ("lex","exclusive"),
    ("yacc","exclusive")
)

reserved = {
    "return": "RETURN",
    "error": "ERROR",
    "%literals": "LITERALS",
    "%ignore": "IGNORE",
    "%tokens": "TOKENS",
    "%precedence": "PRECED"
}

tokens = ["LEX","YACC","PY","RES","TYPE","STR"] + list(reserved.values())

literals = ["[","]","(",")",",","="]
t_ignore = " \t\n\r"

def t_LEX(t):
    r"%%\s?LEX"
    t.lexer.push_state("lex")
    pass

def t_lex_RETURN(t):
    r"return"
    return t

def t_lex_ERROR(t):
    r"error"
    return t

def t_lex_LITERALS(t):
    r"%literals"
    return t

def t_lex_STR():
    r"[fr]?(\".*\"|\'.*\')"

def t_lex_RES(t):
    r"t(\.\w+)+(\(\d*\))?"
    return t

def t_lex_yacc_VAL(t):
    r"(\".*\")|(\'.*\')"
    return t

def t_lex_TYPE(t):
    r"\w+"

def t_lex_YACC(t):
    r"%%\s?YACC"
    t.lexer.pop_state()
    t.lexer.push_state("yacc")
    pass


def t_yacc_RES(t):
    r"{.*}"
    return t

def t_yacc_PY(t):
    r"%%"
    t.lexer.pop_state()
    pass

def t_PY(t):
    r"(.|\n)*"

def t_error(t):
    print("Illegal Character: ", t.value[0])

lexer = lex.lex()