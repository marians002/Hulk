from pycompiler import Grammar

G = Grammar()

# Terminals
semi, comma, dot, colon = G.Terminals("; , . :")
andt, ort, nott = G.Terminals("& | !")
opar, cpar, ocur, ccur, obr, cbr, rarrow, at, sharp, dstr_assign = G.Terminals("( ) { } [ ] => @ # :=")
equal, plus, minus, star, div, sqr, mod, less, leq, great, geq, noteq, eqeq = G.Terminals("= + - * / ^ % < <= > >= != ==")

new, inherits, self, typet, function, protocol, extends = G.Terminals("new inherits self type function protocol extends")
ift, elset, elift, whilet, fort, ranget, let, inx, ist, asx = G.Terminals("if else elif while for range let in is as")
identifier, number, string, boolean = G.Terminals("identifier number string bool")
sqrt, log, exp, sin, cos, rand, PI, E = G.Terminals("sqrt log exp sin cos rand PI E")
true, false = G.Terminals("true false")
printt = G.Terminal("print")

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
type_decl, function_decl, protocol_decl, method_decl = G.NonTerminals("<type_decl> <function_decl> <protocol_decl> <method_decl>")
method_decl_col, typed_method_decl_list, typed_method_decl = G.NonTerminals("<method_decl_col> <typed_method_decl_list> <typed_method_decl>")
cond, loop, assignment, arith = G.NonTerminals("<condition> <loop> <assignment> <arith_expr>")

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

exp_block %= ocur + statement_list + ccur

statement_list %= G.Epsilon  # check consequences of this every time
# statement_list %= statement
statement_list %= statement + statement_list

statement %= simple_exp + semi