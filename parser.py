import ply.yacc as yacc
from lexer import tokens, literals

def p_ply(p):
    """ply : lex yacc PY"""

def p_lex(p):
    """lex : lentries"""

def p_lentries(p):
    """lentries : lentries lentry
                |"""

def p_lentry(p):
    """lentry : '%' lVar
              | lFunc"""

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
    """lPrecedencesElem : lPrecedencesElem , PrecedencesElem
                  | PrecedencesElem """

def p_precedencesElem(p):
    """precedencesElem : '(' LStr ')' """


def p_symboltable(p):
    """symboltable : TEXT '=' '{' dictEntry '}' """

def p_dictEntry(p):
    """dictEntry : STR ':' '{' dictEntry '}'
          | STR ':' type
          |"""

parser = yacc.yacc()