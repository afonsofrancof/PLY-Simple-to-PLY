from re import T
import ply.lex as lex

states = (
    ("lex", "exclusive"),
    ("yacc", "exclusive")
)

reserved = {
    "return": "RETURN",
    "error": "ERROR",
    "%literals": "LITERALS",
    "%ignore": "IGNORE",
    "%tokens": "TOKENS",
    "%reserved": "RESERVED",
    "%precedence": "PRECEDENCE",
    "%prec": "PREC",
    "int": "INT",
    "float": "FLOAT"
}

tokens = ["LEX", "YACC", "PY", "RES", "STR", "COM",
          "UCASE", "ID", "LIT", "PVAR"] + list(reserved.values())

literals = ["[", "]", "(", ")", ",", "=", "%", ":", "{", "}"]
t_ANY_ignore = " \t\n\r"


def t_ANY_COM(t):
    r"[#].*\n"
    pass


def t_LEX(t):
    r"%%\s?LEX"
    t.lexer.push_state("lex")
    pass


def t_lex_STR(t):
    r"[fr]?(\"[^\"]*\"|\'[^']*\')"
    return t


def t_lex_RES(t):
    r"t(\.\w+)+(\(\d*\))?"
    return t


def t_lex_YACC(t):
    r"%%\s?YACC"
    t.lexer.pop_state()
    t.lexer.push_state("yacc")
    pass


def t_yacc_UCASE(t):
    r"[A-Z][A-Z0-9_]*"
    return t


def t_lex_yacc_PVAR(t):
    r"%[a-z]+"
    t.type = reserved.get(t.value, "PVAR")
    if t.type != "PREC":
        t.value = t.value[1:]
    return t


def t_lex_yacc_ID(t):
    r"[a-zA-Z_]\w*"
    t.type = reserved.get(t.value, "ID")
    return t


def t_yacc_LIT(t):
    r"\'.\'"
    return t


# alterar expression para casos em que tenha codigo multiline dentro das {}
def t_yacc_RES(t):
    r"{.*}"
    return t


def t_yacc_STR(t):
    r"[fr]?(\"[^\"]*\"|\'[^']*\')"
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

