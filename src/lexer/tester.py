from lexer_generator import Lexer
tokens = [
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
    ("id_", '[_a-z][_a-zA-Z0-9]*'),
    
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
]
text = """type Person() {
                            name = "John";
                            age = 25;
                            
                           printName(){
                                print(name);
                            }
                        }
                        
                        let x = new Person() in if (x.name == "Jane") print("Jane") else print("John");
               """

lexer = Lexer(tokens,"$")


print([token for token in lexer._tokenize(text)])