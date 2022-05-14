import ply.yacc as yacc
from lexer import tokens, literals
import pprint
import json


def p_ply(p):
    "ply : lex yacc PY"
    p.parser.ts["py"] = p[3]


def p_lex(p):
    "lex : lentries"


def p_lentries_multiple(p):
    "lentries : lentries lentry"


def p_lentries_empty(p):
    "lentries : lentry"


def p_lentry_lfunc(p):
    "lentry : lFunc "
    p.parser.ts["lex"]["funcs"].append(p[1])


def p_lentry_lvar(p):
    "lentry : lVar"


def p_lVar_literals_str(p):
    "lVar : LITERALS '=' STR"
    res = f"{p[1]} = {p[3]}\n\n"
    print(res)
    p.parser.ts["lex"]["vars"]["literals"] = res


def p_lVar_literals_list(p):
    "lVar : LITERALS '=' '[' lStr ']'"
    res = f"{p[1]} = {p[4]}\n\n"
    p.parser.ts["lex"]["vars"]["literals"] = res


def p_lVar_ignore(p):
    "lVar : IGNORE '=' STR"
    res = f"{p[1]} = {p[3]}\n\n"
    p.parser.ts["lex"]["vars"]["ignore"] = res


def p_lVar_tokens(p):
    "lVar : TOKENS '=' list"
    res = f"{p[1]} = {p[3]}\n\n"
    p.parser.ts["lex"]["vars"]["tokens"] = res


def p_list(p):
    "list : '[' lStr ']'"
    p[0] = p[1] + p[2] + p[3]


def p_lStr_multiple(p):
    "lStr : lStr ',' elem"
    p[0] = p[1] + p[2] + p[3]


def p_lStr_single(p):
    "lStr : elem"
    p[0] = p[1]


def p_elem_str(p):
    "elem : STR"
    p[0] = p[1]


def p_elem_char(p):
    "elem : LIT"
    p[0] = p[1]


def p_lFunc_return(p):
    "lFunc : STR RETURN '(' STR ',' res ')'"
    striped_name = p[4].strip("\'\"")
    res = f"def t_{striped_name}(t):\n\t{p[1]}\n"
    if p[6] != "t.value":
        res += f"\t{p[6]}"
    p[0] = res + "\treturn t\n\n"


def p_lFunc_error(p):
    "lFunc : STR ERROR '(' STR ',' RES ')' "
    p[0] = f"def t_error(t):\n\tprint({p[1]})\n\t{p[6]}\n\n"


def p_res_single(p):
    "res : RES"
    p[0] = p[1]


def p_res_with_type(p):
    "res : type '(' RES ')'"
    p[0] = f"t.value = {p[1]}({p[3]})\n"


def p_type_int(p):
    "type : INT"
    p[0] = p[1]


def p_type_float(p):
    "type : FLOAT"
    p[0] = p[1]


def p_yacc(p):
    "yacc : yentries"


def p_yentries_entries(p):
    "yentries : yentries yentry"


def p_yentries_single(p):
    "yentries : yentry"


def p_yentry_yvar(p):
    "yentry : yvar"
    p.parser.ts["yacc"]["vars"].append(p[1])


def p_yentry_rules(p):
    "yentry : rules RES"
    res = p[2].strip("{} ")
    rule = f"{p[1]}\t{res}\n\n"
    p.parser.ts["yacc"]["rules"].append(rule)


def p_yentry_gvar(p):
    "yentry : gvar"
    p.parser.ts["yacc"]["vars"].append(p[1])


def p_yvar_preced(p):
    "yvar : PRECEDENCE '=' '[' lPrecedencesElem ']'"
    p[0] = f"{p[1]} {p[2]} {p[3]}\n{p[4]}\n{p[5]}\n\n"


def p_lPrecedencesElem_multiple(p):
    "lPrecedencesElem : lPrecedencesElem ',' precedencesElem"
    p[0] = p[1] + ",\n" + p[3]


def p_lPrecedencesElem_single(p):
    "lPrecedencesElem : precedencesElem"
    p[0] = p[1]


def p_precedencesElem(p):
    "precedencesElem : '(' lStr ')' "
    p[0] = p[1] + p[2] + p[3]


def p_gvar(p):
    "gvar : ID '=' RES"
    p[0] = f"{p[1]} = {p[3]}\n"


def p_rules(p):
    "rules : ID ':' syms "
    var = f"\"{p[1]}\""
    num = 0
    if var in parser.nametracker:
        num = parser.nametracker.get(var)
    parser.nametracker[var] = num + 1
    header = f"def p_{p[1]}_{num}(t):\n"
    p[0] = f"{header}\t\"{p[1]} : {p[3]}\"\n"


def p_syms_multiple(p):
    "syms : syms sym"
    p[0] = f"{p[1]} {p[2]}"


def p_syms_single(p):
    "syms : sym "
    p[0] = p[1]


def p_sym_ucase(p):
    "sym : UCASE"
    p[0] = p[1]


def p_sym_id(p):
    "sym : ID"
    p[0] = p[1]


def p_sym_lit(p):
    "sym : LIT"
    p[0] = p[1]


def p_sym_prec(p):
    "sym : PREC"
    p[0] = p[1]


def p_error(p):
    print("ERROR", p, "\n", p.value, "\n", p.type, "\n", p.lineno)


parser = yacc.yacc()
parser.nametracker = {}
parser.ts = {"lex": {
    "vars": {"literals": '',
             "tokens": '',
             "ignore": ''
             },
    "funcs": []
},
    "yacc": {
    "vars": [],
    "rules": []
},
    "py": ""
}


def write_to_file():
    header_lex = "import ply.lex as lex\n"
    header_yacc = "import ply.yacc as yacc\n\n"
    f_out.write(header_lex + header_yacc)
    elem = parser.ts["lex"]
    for var in elem["vars"].values():
        f_out.write(var)
    for func in elem["funcs"]:
        f_out.write(func)
    f_out.write("lexer = lex.lex()\n\n")
    elem = parser.ts["yacc"]
    for var in elem["vars"]:
        f_out.write(var)
    for rule in elem["rules"]:
        f_out.write(rule)
    f_out.write(parser.ts["py"])


f = open('exemplo.in', 'r')
f_out = open('exemplo.py', 'w')
text = f.read()
parser.parse(text)

write_to_file()

f.close()
f_out.flush()
f_out.close()
print(json.dumps(parser.ts, sort_keys=False, indent=4))
