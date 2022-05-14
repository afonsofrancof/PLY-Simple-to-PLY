import ply.yacc as yacc
from lexer import tokens, literals


def p_ply(p):
    """ply : lex yacc PY """


def p_lex(p):
    """lex : lentries"""


def p_lentries(p):
    """lentries : lentries lentry
                | """


def p_lentry(p):
    """lentry : '%' lVar
              | lFunc """


def p_lVar(p):
    """lVar : LITERALS '=' STR
            | LITERALS '=' '[' lStr ']'
            | IGNORE '=' STR
            | TOKENS '=' '[' lStr ']' """


def p_lStr(p):
    """lStr : lStr ',' STR
            | STR """


def p_lFunc(p):
    """lFunc : STR RETURN '(' STR ',' res ')'
             | STR ERROR '(' STR ',' RES ')' """


def p_res(p):
    """res : type '(' RES ')'
           | RES """


def p_type(p):
    """type : INT
            | FLOAT """


def p_yacc(p):
    """yacc : precedences symboltable rules """


def p_precedences(p):
    """precedences : PRECEDENCE '=' '[' lPrecedencesElem ']' """


def p_lPrecedencesElem(p):
    """lPrecedencesElem : lPrecedencesElem ',' precedencesElem
                        | precedencesElem """


def p_precedencesElem(p):
    """precedencesElem : '(' lStr ')' """


def p_symboltable(p):
    """symboltable : TEXT '=' '{' RES '}' """


def p_rules(p):
    """rules : SNT ':' syms """


def p_syms(p):
    """syms : syms sym
            | sym """


def p_sym(p):
    """sym : ST
           | SNT
           | STR """

def p_error(p):
    print("ERROR", p, "\n", p.value, "\n", p.type, "\n", p.lineno)


parser = yacc.yacc()
parser.ts = {}

f = open('exemplo.in', 'r')
text = f.read()
parser.parse(text)

