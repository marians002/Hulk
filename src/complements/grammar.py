from pycompiler import Grammar
from ast_for_hulk import *

G = Grammar()

# Terminals
semi, comma, dot, colon = G.Terminals("; , . :")
andt, ort, nott = G.Terminals("& | !")
opar, cpar, ocur, ccur, obr, cbr = G.Terminals("( ) { } [ ]")
rarrow, at, atat, sharp, dstr_assign, dble_bar = G.Terminals("=> @ @@ # := ||")
equal, plus, minus, star, starstar, div, sqr, mod = G.Terminals("= + - * ** / ^ %")
less, leq, great, geq, noteq, eqeq = G.Terminals("< <= > >= != ==")

new, inherits, self, typet = G.Terminals("new inherits self type")
function, protocol, extends = G.Terminals("function protocol extends")
ift, elset, elift, whilet, fort, ranget, let, inx, ist, asx = G.Terminals("if else elif while for range let in is as")
identifier, number, string, boolean = G.Terminals("identifier number string bool")

# Non-Terminals
program = G.NonTerminal("<program>", True)
global_exp = G.NonTerminal("<global_exp>")

declaration, decl_list = G.NonTerminals("<declaration> <decl_list>")
statement, statement_list = G.NonTerminals("<statement> <statement_list>")
params, params_list = G.NonTerminals("<params> <params_list>")
typed_params, typed_params_list = G.NonTerminals("<typed_params> <typed_params_list>")
attr, attr_list = G.NonTerminals("<attr> <attr_list>")
args, args_list = G.NonTerminals("<args> <args_list>")
simple_exp, exp_block = G.NonTerminals("<exp> <exp_block>")
type_decl, function_decl, protocol_decl, method_decl = G.NonTerminals(
    "<type_decl> <function_decl> <protocol_decl> <method_decl>")
method_decl_col, typed_method_decl_list, typed_method_decl = G.NonTerminals(
    "<method_decl_col> <typed_method_decl_list> <typed_method_decl>")
molecule, atom = G.NonTerminals("<molecule> <atom>")
elifn, var_decl = G.NonTerminals("<elifn> <var_decl>")
string_exp, single_exp = G.NonTerminals("<string_exp> <single_exp>")
condition, disjunction, not_comp_exp, comparer = G.NonTerminals("<condition> <disjunction> <not_comp_exp> <comparer>")
arith, term, factor, unary_exp = G.NonTerminals("<arith_expr> <term> <factor> <unary_exp>")
invoque_func = G.NonTerminal("<invoque_func>")
loop, assignment = G.NonTerminals("<loop> <assignment>")

# Productions
program %= decl_list + global_exp, lambda h, s: ProgramNode(s[1], s[2])

decl_list %= G.Epsilon, lambda h, s: []
decl_list %= declaration + decl_list, lambda h, s: [s[1]] + s[2]

declaration %= function_decl, lambda h, s: s[1]
declaration %= type_decl, lambda h, s: s[1]
declaration %= protocol_decl, lambda h, s: s[1]

function_decl %= function + identifier + opar + params + cpar + rarrow + statement, lambda h, s: FunctionNode(s[2], s[4], None, s[7])
function_decl %= function + identifier + opar + params + cpar + exp_block, lambda h, s: FunctionNode(s[2], s[4], None, s[6])
function_decl %= function + identifier + opar + params + cpar + colon + identifier + rarrow + statement, lambda h, s: FunctionNode(s[2], s[4], s[7], s[9])
function_decl %= function + identifier + opar + params + cpar + colon + identifier + exp_block, lambda h, s: FunctionNode(s[2], s[4], s[7], s[8])

method_decl %= identifier + opar + params + cpar + rarrow + statement, lambda h, s: FunctionNode(s[1], s[3], None, s[6])
method_decl %= identifier + opar + params + cpar + exp_block, lambda h, s: FunctionNode(s[1], s[3], None, s[5])
method_decl %= identifier + opar + params + cpar + colon + identifier + rarrow + statement, lambda h, s: FunctionNode(s[1], s[3], s[6], s[8])
method_decl %= identifier + opar + params + cpar + colon + identifier + exp_block, lambda h, s: FunctionNode(s[1], s[3], s[6], s[7])

params %= G.Epsilon, lambda h, s: []
params %= params_list, lambda h, s: s[1]

params_list %= identifier, lambda h, s: [DeclareVariableNode(s[1], None, None)]
params_list %= identifier + comma + params_list, lambda h, s: [DeclareVariableNode(s[1], None, None)] + s[3]
params_list %= identifier + colon + identifier, lambda h, s: [DeclareVariableNode(s[1], s[3], None)]
params_list %= identifier + colon + identifier + comma + params_list, lambda h, s: [DeclareVariableNode(s[1], s[3], None)] + s[5]

# type Person {...}
type_decl %= typet + identifier + ocur + attr_list + ccur, lambda h, s: TypeNode(s[2], None, [None], [], s[4])
# type Person(x,y) {...}
type_decl %= typet + identifier + opar + params + cpar + ocur + attr_list + ccur, lambda h, s: TypeNode(s[2], None, s[4], [], s[7])
# type Person inherits Human {...}
type_decl %= typet + identifier + inherits + identifier + ocur + attr_list + ccur, lambda h, s: TypeNode(s[2], s[4], [], [], s[6])
# type Person(x,y) inherits Human {...}   ********** QUIZAS INNECESARIA **********
type_decl %= typet + identifier + opar + params + cpar + inherits + identifier + ocur + attr_list + ccur, lambda h, s: TypeNode(s[2], s[7], s[4], [], s[9])
# type Person(x,y) inherits Human(x,y) {...}
type_decl %= typet + identifier + opar + params + cpar + inherits + identifier + opar + args + cpar + ocur + attr_list + ccur, lambda h, s: TypeNode(s[2], s[7], s[4], s[9], s[12])

attr_list %= G.Epsilon, lambda h, s: []
attr_list %= attr + attr_list, lambda h, s: [s[1]] + s[2]

attr %= identifier + equal + statement, lambda h, s: DeclareVariableNode(s[1], None, s[3])
attr %= identifier + colon + identifier + equal + statement, lambda h, s: DeclareVariableNode(s[1], s[3], s[5])
attr %= method_decl, lambda h, s: s[1]

protocol_decl %= protocol + identifier + method_decl_col
protocol_decl %= protocol + identifier + extends + identifier + method_decl_col

method_decl_col %= ocur + typed_method_decl_list + ccur

typed_method_decl_list %= G.Epsilon
typed_method_decl_list %= typed_method_decl + typed_method_decl_list

typed_method_decl %= identifier + opar + typed_params + cpar + colon + identifier + semi

typed_params %= G.Epsilon
typed_params %= typed_params_list

typed_params_list %= identifier + colon + identifier
typed_params_list %= identifier + colon + identifier + comma + typed_params_list

global_exp %= statement, lambda h, s: s[1]
global_exp %= exp_block, lambda h, s: s[1]

statement %= simple_exp + semi, lambda h, s: s[1]

exp_block %= ocur + statement_list + ccur, lambda h, s: BlockNode(s[2])

statement_list %= G.Epsilon, lambda h, s: []  # check consequences of this every time
# statement_list %= statement
statement_list %= statement + statement_list, lambda h, s: [s[1]] + s[2]

simple_exp %= single_exp, lambda h, s: s[1]
simple_exp %= new + identifier + opar + args + cpar, lambda h, s: NewNode(s[2], s[4])
simple_exp %= molecule + assignment + simple_exp, lambda h, s: AssignNode(s[1], s[3])
simple_exp %= let + var_decl + inx + simple_exp, lambda h, s: LetNode(s[2], s[4])
simple_exp %= whilet + opar + condition + cpar + simple_exp, lambda h, s: WhileNode(s[3], s[5])
simple_exp %= fort + opar + identifier + inx + simple_exp + cpar + simple_exp, lambda h, s: ForNode(DeclareVariableNode(s[3], None, None), s[5], s[7])
simple_exp %= ift + opar + condition + cpar + simple_exp + elifn + elset + simple_exp, lambda h, s: IfNode([(s[3], s[5])] + s[6] + [(BoolNode(True), s[8])])

single_exp %= string_exp, lambda h, s: s[1]
single_exp %= string_exp + asx + identifier, lambda h, s: AsNode(s[1], s[3])

elifn %= G.Epsilon, lambda h, s: []
elifn %= elift + opar + condition + cpar + simple_exp + elifn, lambda h, s: [(s[3], s[5])] + s[6]

var_decl %= identifier + equal + simple_exp, lambda h, s: [DeclareVariableNode(s[1], None, s[3])]
var_decl %= identifier + equal + simple_exp + comma + var_decl, lambda h, s: [DeclareVariableNode(s[1], None, s[3])] + s[5]
var_decl %= identifier + colon + identifier + equal + simple_exp, lambda h, s: [DeclareVariableNode(s[1], s[3], s[5])]
var_decl %= identifier + colon + identifier + equal + simple_exp + comma + var_decl, lambda h, s: [DeclareVariableNode(s[1], s[3], s[5])] + s[7]

string_exp %= condition, lambda h, s: s[1]
string_exp %= string_exp + at + condition, lambda h, s: ConcatNode(s[1], s[3])
string_exp %= string_exp + atat + condition, lambda h, s: ConcatNode(s[1], s[3])

condition %= disjunction, lambda h, s: s[1]
condition %= condition + andt + disjunction, lambda h, s: AndNode(s[1], s[3])

disjunction %= not_comp_exp, lambda h, s: s[1]
disjunction %= condition + ort + not_comp_exp, lambda h, s: OrNode(s[1], s[3])

not_comp_exp %= comparer, lambda h, s: s[1]
not_comp_exp %= nott + comparer

comparer %= arith, lambda h, s: s[1]
comparer %= arith + eqeq + arith
comparer %= arith + noteq + arith
comparer %= arith + less + arith
comparer %= arith + leq + arith
comparer %= arith + great + arith
comparer %= arith + geq + arith
comparer %= arith + ist + identifier

arith %= term, lambda h, s: s[1]
arith %= arith + plus + term
arith %= arith + minus + term

term %= unary_exp, lambda h, s: s[1]
term %= term + star + unary_exp
term %= term + div + unary_exp
term %= term + mod + unary_exp

unary_exp %= factor, lambda h, s: s[1]
unary_exp %= minus + unary_exp

factor %= molecule, lambda h, s: s[1]
factor %= molecule + sqr + factor
factor %= molecule + starstar + factor

molecule %= atom, lambda h, s: s[1]
molecule %= molecule + dot + invoque_func
molecule %= molecule + dot + identifier
molecule %= molecule + obr + simple_exp + cbr

atom %= identifier, lambda h, s: VarNode(s[1])
atom %= number, lambda h, s: NumberNode(s[1])
atom %= string, lambda h, s: BoolNode(s[1])
atom %= boolean, lambda h, s: StringNode(s[1])
atom %= invoque_func, lambda h, s: s[1]
atom %= exp_block, lambda h, s: s[1]
atom %= opar + simple_exp + cpar, lambda h, s: s[2]
atom %= obr + args + cbr
atom %= obr + simple_exp + dble_bar + identifier + inx + simple_exp + cbr

invoque_func %= identifier + opar + args + cpar

args %= G.Epsilon, lambda h, s: []
args %= simple_exp + args_list

args_list %= G.Epsilon, lambda h, s: []
args_list %= comma + simple_exp + args_list

