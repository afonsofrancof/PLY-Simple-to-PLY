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

tokens = ["LEX","YACC","VAL","PY","RES","TYPE"] + list(reserved.values())

literals = ["[","]","(",")",",","="]
ignore = " \t\n\r"

t_RETURN = r"return"

def t_LEX(t):
    r"%% LEX"
    t.lexer.push_state("lex")
    pass

def t_lex_    

def t_lex_yacc_VAL(t):
    r"(\".*\")|(\'.*\')"
    return t

def t_lex_TYPE(t):
    r"\w+"

def t_lex_YACC(t):
    r"%% YACC"
    t.lexer.pop_state()
    t.lexer.push_state("yacc")
    pass



def t_yacc_RES(t):
    r"{.*}"
    return t

def t_PY(t):
    r"(.|\n)*"

def t_error(t):
    print("Illegal Character: ", t.value[0])

lexer = lex.lex()