from pycompiler import Grammar

G = Grammar()

# Terminals
semi, comma, dot = G.Terminals("; , .")
andt, ort, nott = G.Terminals("& | !")
opar, cpar, ocur, ccur, obr, cbr, rarrow, at, sharp, dstr_assign = G.Terminals("( ) { } [ ] => @ # :=")
equal, plus, minus, star, div, sqr, mod, less, leq, great, geq, noteq, eqeq = G.Terminals("= + - * / ^ % < <= > >= != ==")

new, inherits, self, type, function, protocol = G.Terminals("new inherits self type function protocol")
ift, elset, elift, whilet, fort, ranget, let, inx = G.Terminals("if else elif while for range let in")
sqrt, log, exp, sin, cos, rand, PI, E = G.Terminals("sqrt log exp sin cos rand PI E")
true, false = G.Terminals("true false")
printt = G.Terminals("print")

# Non-Terminals
program = G.NonTerminal("<program>", True)

decl_list, declaration = G.NonTerminals("<decl_list> <declaration>")
type_decl, function_decl, protocol_decl = G.NonTerminals("<type_decl> <function_decl> <protocol_decl>")
cond, loop, assignment, arith = G.NonTerminals("<condition> <loop> <assignment> <arith_expr>")
params, params_list = G.NonTerminals("<params> <params_list>")

# Productions
program %= decl_list

decl_list %= G.Epsilon
decl_list %= declaration + decl_list

declaration %= type_decl
declaration %= function_decl
declaration %= protocol_decl

print(G)

# Non-Terminals
# S = G.NonTerminal('S', True)  # Start symbol
# Assignment = G.NonTerminal('Assignment')
# IfElse = G.NonTerminal('IfElse')
# Print = G.NonTerminal('Print')
# Expression = G.NonTerminal('Expression')
# Block = G.NonTerminal('Block')
#
# # Productions
# S %= Assignment + in_ + Block
# Assignment %= let + identifier + equal + Expression
# Expression %= identifier + mod + number + eqeq + number
# IfElse %= if_ + lpar + Expression + rpar + lcur + Print + semi + Print + semi + rcur + else_ + Print + semi
# Print %= print_ + lpar + (identifier | string) + rpar
# Block %= IfElse


