from cmp.grammar import *

HULK_TOKENS = [
    (semi, ';'),
    (comma, ','),
    (dot, '\.'),
    (colon, ':'),
    
    (andt, '&'), 
    (ort, '\|'), 
    (nott, '!'),
    (dble_bar, '\|\|'),
    
    (opar, '\('), 
    (cpar, '\)'), 
    (ocur, '\{'), 
    (ccur, '\}'), 
    (obr, '\['), 
    (cbr, '\]'),
    
    
    (at, '@'), 
    (atat, '@@'), 
    (sharp, '#'), 
    
    (dstr_assign, ':='), 
    (equal, '='), 
    (new, 'new'), 
    
    (plus, '\+'), 
    (minus, '\-'), 
    (star, '\*'), 
    (div, '/'), 
    (sqr, '\^'), 
    (starstar, '\*\*'), 
    (mod, '%'),           
    
    (less, '<'), 
    (leq, '<='), 
    (great, '>'), 
    (geq, '>='), 
    (noteq, '!='), 
    (eqeq, '=='),
    
               
    (inherits, 'inherits'),            
    (extends, 'extends'),
    (typet, 'type'),
    
    (function, 'function'), 
    (rarrow, '=>'), 
    (protocol, 'protocol'), 
    
    (ift, 'if'), 
    (elset, 'else'), 
    (elift, 'elif'), 
    (whilet, 'while'), 
    (fort , 'for'), 
    (let, 'let'), 
    
    (inx, 'in'), 
    (ist, 'is'),            
    (asx, 'as'),
    
    (identifier, '[_a-zA-Z][_a-zA-Z0-9]*'),        
    (number, '(0|[1-9]([0-9])*)(\.[0-9]+)?'),
    (string, '"([\x00-!#-\x7f]|\\\\")*"'), 
    (boolean, 'true|false'),
    ("space", ' '),
    ("endofline", '\n'),
    ("tab", '\t' )
    ]

HULK_TOKENS.append(('comment','//[\x00-\x09\x0b-\x7f]*\n'))

