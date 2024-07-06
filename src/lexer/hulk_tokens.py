HULK_TOKENS = [
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
    
    ("bool_", 'true|false'),
    ("str_", '"([\x00-!#-\x7f]|\\\\")*"'),
    ("number_", '(0|[1-9][0-9]*)(.[0-9]+)?'),
    
    
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
    ("endofline_",'\n'),
    ("id_", '[_a-zA-Z][_a-zA-Z0-9]*'),
    
]
HULK_TOKENS.append(('comment','//[\x00-\x09\x0b-\x7f]*\n'))
HULK_TOKENS.append(('space', '  *'))