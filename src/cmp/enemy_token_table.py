from cmp.enemy_grammar import *


sym = [  
    ',',
    ':',
    ';',
    '<',
    '>',
    '!',
    '=',
    '\?',
    '%',
    '.',
    '\'',
    ' ',
    '\n',
    '\t',
    r'\\"'
    ]
symbols = '|'.join(str(n) for n in sym)
nonzero_digits = '|'.join(str(n) for n in range(1,10))
zero_digits = '|'.join(str(n) for n in range(0,10))
letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))
letters += letters.join('|')
letters += '|'.join(chr(n) for n in range(ord('A'),ord('Z')+1))
alphanumeric = f'{letters}|{zero_digits}'+'|'+'_'
alphanumeric_with_symbols= alphanumeric+'|'+symbols

""" table = [
    (string_, '"([\x00-!#-\x7f]|\\\\")*"'),
    (PI_const_, 'PI'),
    (E_const_ ,'E'),
    (plus_, '\+'),
    (minus_, '\-'),
    (pow_, '^|(\*\*)'),
    (times_, '\*'),
    (div_, '/'),
    (mod_,'%'),
    (opar_, '\('),
    (cpar_, '\)'),
    (obracket_, '\{'),
    (cbracket_, '\}'),
    (semicolon_, ';'),
    (colon_, ':'),
    (coma_, ','),
    (dot_,'\.'),
    (equals_, '='),
    (destr_assign_,':='),
    (true_,'true'),
    (false_,'false'),
    (and_logic_c_,'&'),
    (or_logic_c_,'\|'),
    (not_logic_c_,'!'),
    (doubleequals_c_,'=='),
    (different_c_,'!='),
    (lt_c_,'<'),
    (gt_c_,'>'),
    (let_c_,'<='),
    (get_c_,'>='),
    (if_,'if'),
    (else_,'else'),
    (elif_,'elif'),
    (let_ , 'let'),
    (in_ , 'in'), 
    (as_, 'as'),
    (is_, 'is'),
    (while_,'while'),
    (for_,'for'),
    (range_,'range'),
    (function_,'function'),
    (arrow_,'=>'),
    (new_,'new'),
    (type_,'type'),
    (inherits_, 'inherits'),
    (self_, 'self'),
    (base_, 'base'),
    (print_,'print'),
    (sqrt_, 'sqrt'),
    (sin_,'sin'),
    (cos_,'cos'),
    (exp_,'exp'),
    (log_,'log'),
    (rand_,'rand'),     
    (id_, '[_a-zA-Z][_a-zA-Z0-9]*'),
    (num_, '(0|[1-9][0-9]*)(\.[0-9]+)?'),
    (at_,'@'),
    (doubleat_,'@@')
] """

table = [
    
    (semicolon_, ';'),
    (num_, '(0|[1-9][0-9]*)(\.[0-9]+)?')
    
]