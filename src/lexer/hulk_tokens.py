""" HULK_TOKENS = [
    ("obra", '\{'),
    ("cbra", '\}'),
    ("opar", '\('),
    ("cpar", '\)'),
    ("ocor", '\['),
    ("ccor", '\]'),
    ("d_bar", '\|\|'),
    
    ("dot", '\.'),
    ("semi", ','),
    ("colon", ':'),
    ("semicolon", ';'),
    ("arrow", '=>'),
    
    ("or_", '\|'),
    ("and_", '&'),
    ("not_", '!'),
    
    ("d_as", ':='),
    ("s_as", '='),
    ("new_", 'new'),
    
    ("eq", '=='),
    ("neq", '!='),
    ("leq", '<='),
    ("geq", '>='),
    ("lt", '<'),
    ("gt", '>'),
    
    ("is_", 'is'),
    ("as_", 'as'),
    
    ("arr", '@'),
    ("d_arr", '@@'),
    
    ("plus", '\+'),
    ("minus", '\-'),
    ("star", '\*'),
    ("div", '/'),
    ("mod", '%'),
    ("pow_", '\^'),
    ("pow__", '\*\*'),
    
    ("let_", 'let'),
    ("in_", 'in'),
    
    ("if_", 'if'),
    ("else_", 'else'),
    ("elif_", 'elif'),
    
    ("while_", 'while'),
    ("for_", 'fo'),
    
    ("inherits", 'inherits'),
    ("function", 'function'),
    ("protocol", 'protocol'),
    ("extends", 'extends'),
    ("type_", 'type'),
    ("base_", 'base'),
    
    ("bool", 'true|false'),
    ("string", '"([\x00-!#-\x7f]|\\\\")*"'),
    ("number", '(0|[1-9][0-9]*)(.[0-9]+)?'),
    
    ("endofline_",'\n'),
    ("identifier", '[_a-zA-Z][_a-zA-Z0-9]*'),
    
]
HULK_TOKENS.append(('comment','//[\x00-\x09\x0b-\x7f]*\n'))
HULK_TOKENS.append(('space', '  *')) """

HULK_TOKENS = [
    ("semi", ';'),
    ("comma", ','),
    ("dot", '\.'),
    ("colon", ':'),
    
    ("andt", '&'), 
    ("ort", '\|'), 
    ("nott", '!'),
    ("dble_bar", '\|\|'),
    
    ("opar", '\('), 
    ("cpar", '\)'), 
    ("ocur", '\{'), 
    ("ccur", '\}'), 
    ("obr", '\['), 
    ("cbr", '\]'),
    
    
    ("at", '@'), 
    ("atat", '@@'), 
    ("sharp", '#'), 
    
    ("dstr_assign", ':='), 
    ("equal", '='), 
    ("new", 'new'), 
    
    ("plus", '\+'), 
    ("minus", '\-'), 
    ("star", '\*'), 
    ("starstar", '\*\*'), 
    ("div", '/'), 
    ("sqr", '\^'), 
    ("mod", '%'),           
    
    ("less", '<'), 
    ("leq", '<='), 
    ("great", '>'), 
    ("geq", '>='), 
    ("noteq", '!='), 
    ("eqeq", '=='),
    
               
    ("inherits", 'inherits'),            
    ("extends", 'extends'),
    ("self", 'self'), 
    ("typet", 'type'),
    
    ("function", 'function'), 
    ("rarrow", '=>'), 
    ("protocol", 'protocol'), 
    
    ("ift", 'if'), 
    ("elset", 'else'), 
    ("elift", 'elif'), 
    ("whilet", 'while'), 
    ("fort", 'for'), 
    ("ranget", 'range'), 
    ("let", 'let'), 
    
    ("inx", 'in'), 
    ("ist", 'is'),            
    ("asx", 'as'),
        
    ("identifier", '[_a-zA-Z][_a-zA-Z0-9]'),        
    ("number", '(0|[1-9][0-9])(.[0-9]+)?'),
    ("string", '"([\x00-!#-\x7f]|\\\\")*"'),
    ("boolean", 'true|false')
    ]

HULK_TOKENS.append(('comment','//[\x00-\x09\x0b-\x7f]*\n'))

