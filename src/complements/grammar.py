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
attr, attr_list, attr_list_block = G.NonTerminals("<attr> <attr_list> <attr_list_block>")
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
program %= decl_list + global_exp

decl_list %= G.Epsilon
decl_list %= declaration + decl_list

declaration %= function_decl
declaration %= type_decl
declaration %= protocol_decl

function_decl %= function + identifier + opar + params + cpar + rarrow + statement
function_decl %= function + identifier + opar + params + cpar + exp_block
function_decl %= function + identifier + opar + params + cpar + colon + identifier + rarrow + statement
function_decl %= function + identifier + opar + params + cpar + colon + identifier + exp_block

method_decl %= identifier + opar + params + cpar + rarrow + statement
method_decl %= identifier + opar + params + cpar + exp_block
method_decl %= identifier + opar + params + cpar + colon + identifier + rarrow + statement
method_decl %= identifier + opar + params + cpar + colon + identifier + exp_block

params %= G.Epsilon
params %= params_list

params_list %= identifier
params_list %= identifier + comma + params_list
params_list %= identifier + colon + identifier
params_list %= identifier + colon + identifier + comma + params_list

# type Person {...}
type_decl %= typet + identifier + attr_list_block
# type Person(x,y) {...}
type_decl %= typet + identifier + opar + params + cpar + attr_list_block
# type Person inherits Human {...}
type_decl %= typet + identifier + inherits + identifier + attr_list_block
# type Person inherits Human(x,y) {...}   ********** QUIZAS INNECESARIA **********
type_decl %= typet + identifier + inherits + identifier + opar + args + cpar + attr_list_block
# type Person(x,y) inherits Human {...}   ********** QUIZAS INNECESARIA **********
type_decl %= typet + identifier + opar + params + cpar + inherits + identifier + attr_list_block
# type Person(x,y) inherits Human(x,y) {...}
type_decl %= typet + identifier + opar + params + cpar + inherits + identifier + opar + args + cpar + attr_list_block

attr_list_block %= ocur + attr_list + ccur

attr_list %= G.Epsilon
attr_list %= attr + attr_list

attr %= identifier + equal + statement
attr %= identifier + colon + identifier + equal + statement
attr %= method_decl

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

global_exp %= statement
global_exp %= exp_block

statement %= simple_exp + semi

exp_block %= ocur + statement_list + ccur

statement_list %= G.Epsilon  # check consequences of this every time
# statement_list %= statement
statement_list %= statement + statement_list

simple_exp %= single_exp
simple_exp %= new + identifier + opar + args + cpar
simple_exp %= molecule + assignment + simple_exp
simple_exp %= let + var_decl + inx + simple_exp
simple_exp %= whilet + opar + condition + cpar + simple_exp
simple_exp %= fort + opar + identifier + inx + simple_exp + cpar + simple_exp
simple_exp %= ift + opar + condition + cpar + simple_exp + elifn + elset + simple_exp

single_exp %= string_exp
single_exp %= string_exp + asx + identifier

elifn %= G.Epsilon
elifn %= elift + opar + condition + cpar + simple_exp + elifn

var_decl %= identifier + equal + simple_exp
var_decl %= identifier + equal + simple_exp + comma + var_decl
var_decl %= identifier + colon + identifier + equal + simple_exp
var_decl %= identifier + colon + identifier + equal + simple_exp + comma + var_decl

string_exp %= condition
string_exp %= string_exp + at + condition
string_exp %= string_exp + atat + condition

condition %= disjunction
condition %= condition + andt + disjunction

disjunction %= not_comp_exp
disjunction %= condition + ort + not_comp_exp

not_comp_exp %= comparer
not_comp_exp %= nott + comparer

comparer %= arith
comparer %= arith + eqeq + arith
comparer %= arith + noteq + arith
comparer %= arith + less + arith
comparer %= arith + leq + arith
comparer %= arith + great + arith
comparer %= arith + geq + arith
comparer %= arith + ist + identifier

arith %= term
arith %= arith + plus + term
arith %= arith + minus + term

term %= unary_exp
term %= term + star + unary_exp
term %= term + div + unary_exp
term %= term + mod + unary_exp

unary_exp %= factor
unary_exp %= minus + unary_exp

factor %= molecule
factor %= molecule + sqr + factor
factor %= molecule + starstar + factor

molecule %= atom
molecule %= molecule + dot + invoque_func
molecule %= molecule + dot + identifier
molecule %= molecule + obr + simple_exp + cbr

atom %= identifier
atom %= number
atom %= string
atom %= boolean
atom %= invoque_func
atom %= exp_block
atom %= opar + simple_exp + cpar
atom %= obr + args + cbr
atom %= obr + simple_exp + dble_bar + identifier + inx + simple_exp + cbr

invoque_func %= identifier + opar + args + cpar

args %= G.Epsilon
args %= simple_exp + args_list

args_list %= G.Epsilon
args_list %= comma + simple_exp + args_list

