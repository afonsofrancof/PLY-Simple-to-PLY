import ply.yacc as yacc
from lexer import tokens
import ast


def grammarCheck():
    for elem in parser.rulesCalled:
        if elem not in parser.rulesDefined:
            parser.error = True
            print(
                f"Called rule {elem}, but it's definition could not be found.")
    if not parser.error:
        # print(json.dumps(parser.ts, sort_keys=False, indent=4))
        write_to_file()


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
    "lentry : lFunc"
    p.parser.ts["lex"]["funcs"].append(p[1])


def p_lentry_lvar(p):
    "lentry : lVar"


def p_lVar_literals_str(p):
    "lVar : LITERALS '=' STR"
    res = f"{p[1]} = {p[3]}\n"
    p.parser.ts["lex"]["vars"]["literals"] = res
    for e in p[3][1:-1]:
        p.parser.lex_tokens.add(e)


def p_lVar_literals_list(p):
    "lVar : LITERALS '=' list"
    res = f"{p[1]} = {p[3]}\n"
    p.parser.ts["lex"]["vars"]["literals"] = res
    for e in ast.literal_eval(p[3]):
        p.parser.lex_tokens.add(e)


def p_lVar_ignore(p):
    "lVar : IGNORE '=' STR"
    res = f"t_{p[1]} = {p[3]}\n"
    p.parser.ts["lex"]["vars"]["ignore"] = res


def p_lVar_tokens(p):
    "lVar : TOKENS '=' list"
    res = f"{p[1]} = {p[3]}\n"
    for elem in p[3].strip('[]').split(','):
        p.parser.lex_tokens.add(elem.strip('\'\"'))
    p.parser.ts["lex"]["vars"]["tokens"] = res


def p_lVar_reserved(p):
    "lVar : RESERVED '=' dict"
    res = f"{p[1]} = {p[3]}\n"
    for e in ast.literal_eval(p[3]).values():
        p.parser.lex_tokens.add(e)
    p.parser.ts["lex"]["vars"]["reserved"] = res


def p_list(p):
    "list : '[' lCont ']'"
    p[0] = p[1] + p[2] + p[3]


def p_lCont_multiple(p):
    "lCont : lCont ',' elem"
    p[0] = p[1] + p[2] + p[3]


def p_lCont_single(p):
    "lCont : elem"
    p[0] = p[1]


def p_elem_str(p):
    "elem : STR"
    p[0] = p[1]


def p_elem_char(p):
    "elem : LIT"
    p[0] = p[1]


def p_dict(p):
    "dict : '{' dictElems '}'"
    p[0] = f"{p[1]}\n{p[2]}\n{p[3]}"


def p_dictElems_multiple(p):
    "dictElems : dictElems ',' dictElem"
    p[0] = f"{p[1]}{p[2]}\n{p[3]}"


def p_dictElems_single(p):
    "dictElems : dictElem"
    p[0] = f"{p[1]}"


def p_dictElem(p):
    "dictElem : elem ':' elem"
    p[0] = f"\t{p[1]} {p[2]} {p[3]}"


def p_lFunc_return(p):
    "lFunc : STR RETURN '(' STR ',' res ')'"
    striped_name = p[4].strip("\'\"")
    res = f"def t_{striped_name}(t):\n\t{p[1]}\n"
    if p[6] != "t.value":
        res += f"\t{p[6]}"
    p[0] = res + "\treturn t\n\n"


def p_lFunc_error(p):
    "lFunc : STR ERROR '(' STR ',' RES ')' "
    p[0] = f"def t_error(t):\n\tprint({p[4]})\n\t{p[6]}\n\n"


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
    try:
        ast.parse(res)
    except SyntaxError:
        p.parser.error = True
        print(f"Python syntax error at:\n\t {p[2].strip('{}')}")

    rule = f"{p[1]}\t{res}\n\n"
    p.parser.ts["yacc"]["rules"].append(rule)


def p_yentry_gvar(p):
    "yentry : gvar"
    p.parser.ts["yacc"]["vars"].append(p[1])


def p_yvar_preced(p):
    "yvar : PRECEDENCE '=' precedenceList"
    p[0] = f"{p[1]} {p[2]} {p[3]}\n"


def p_precedenceList(p):
    "precedenceList : '[' precedenceElems ']'"
    p[0] = f"{p[1]}\n{p[2]}\n{p[3]}\n"


def p_precedenceElems_multiple(p):
    "precedenceElems : precedenceElems ',' precedenceElem"
    p[0] = p[1] + ",\n" + p[3]


def p_precedenceElems_single(p):
    "precedenceElems : precedenceElem"
    p[0] = p[1]


def p_precedenceElem(p):
    "precedenceElem : '(' lCont ')' "
    p[0] = '\t' + p[1] + p[2] + p[3]
    for elem in ast.literal_eval(p[2].strip('()'))[1:]:
        p.parser.lex_tokens.add(elem)


def p_gvar(p):
    "gvar : ID '=' RES"
    p[0] = f"{p[1]} = {p[3]}\n"


def p_rules(p):
    "rules : ID ':' syms "
    var = f"\"{p[1]}\""
    num = 0
    if var in p.parser.nametracker:
        num = p.parser.nametracker.get(var)
    p.parser.nametracker[var] = num + 1
    header = f"def p_{p[1]}_{num}(t):\n"
    p[0] = f"{header}\t\"{p[1]} : {p[3]}\"\n"
    parser.rulesDefined.add(p[1])


def p_syms_multiple(p):
    "syms : syms sym"
    p[0] = f"{p[1]} {p[2]}"


def p_syms_single(p):
    "syms : sym "
    p[0] = p[1]


def p_sym_ucase(p):
    "sym : UCASE"
    if p[1] not in p.parser.lex_tokens:
        p.parser.error = True
        print(f"ERROR: Token {p[1]} not declared.")
    p[0] = p[1]


def p_sym_id(p):
    "sym : ID"
    p[0] = p[1]
    parser.rulesCalled.add(p[1])


def p_sym_lit(p):
    "sym : LIT"
    p[0] = p[1]
    if p[1][1:-1] not in p.parser.lex_tokens:
        p.parser.error = True
        print(f"ERROR: Literal {p[1]} not declared.")


def p_sym_prec(p):
    "sym : PREC"
    p[0] = p[1]


def p_error(p):
    print("ERROR", p, "\n", p.value, "\n", p.type, "\n", p.lineno)
    parser.error = True


parser = yacc.yacc()
parser.nametracker = {}
parser.error = False
parser.rulesDefined = set([])
parser.rulesCalled = set([])
parser.lex_tokens = set([])
parser.ts = {
    "lex": {
        "vars": {"literals": '',
                 "reserved": '',
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
    f_out = open('exemplo.py', 'w')
    header_lex = "import ply.lex as lex\n"
    header_yacc = "import ply.yacc as yacc\n\n"
    reserved_append = " + list(reserved.values())\n"
    if parser.ts["lex"]["vars"]["reserved"] != '':
        new_tokens = parser.ts["lex"]["vars"]["tokens"]
        new_tokens = new_tokens[:-1] + reserved_append
        parser.ts["lex"]["vars"]["tokens"] = new_tokens
    f_out.write(header_lex + header_yacc)
    elem = parser.ts["lex"]
    for var in elem["vars"].values():
        f_out.write(var)
    f_out.write("\n")
    for func in elem["funcs"]:
        f_out.write(func)
    f_out.write("lexer = lex.lex()\n\n")
    elem = parser.ts["yacc"]
    for var in elem["vars"]:
        f_out.write(var)
    for rule in elem["rules"]:
        f_out.write(rule)
    f_out.write(parser.ts["py"])
    f_out.flush()
    f_out.close()


f = open('exemplo.in', 'r')
text = f.read()
parser.parse(text)

grammarCheck()

f.close()
