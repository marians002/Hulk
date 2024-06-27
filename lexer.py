# from cmp.tools.automata import NFA, DFA, nfa_to_df
from cmp.tools.automata import  automata_minimization
# from cmp.tools.regex import Regex
from cmp.utils import Token
from cmp.automata import State
from automata import NFA, DFA, nfa_to_dfa, automata_union, automata_concatenation, automata_closure
# from cmp.pycompiler import Grammar
from cmp.tools.parsing import metodo_predictivo_no_recursivo
from cmp.tools.evaluation import evaluate_parse
class Node:
    def evaluate(self):
        raise NotImplementedError()         
class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex
class UnaryNode(Node):
    def __init__(self, node):
        self.node = node        
    def evaluate(self):
        value = self.node.evaluate() 
        return self.operate(value)    
    @staticmethod
    def operate(value):
        raise NotImplementedError()        
class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right        
    def evaluate(self):
        lvalue = self.left.evaluate() 
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)    
    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()

EPSILON = 'ε'
class EpsilonNode(AtomicNode):
    def evaluate(self):
        # Your code here!!!
        return NFA(states=2, finals=[1], transitions={(0, ''): [1]})
class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        return NFA(states=2, finals=[1], transitions={(0, s): [1]})
class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        # Your code here!!!
        return automata_closure(value)
class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        # Your code here!!!
        return automata_union(lvalue,rvalue)
class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        # Your code here!!!
        return automata_concatenation(lvalue,rvalue)
    


G = Grammar()

E = G.NonTerminal('E', True)
T, F, A, X, Y, Z = G.NonTerminals('T F A X Y Z')
pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')

E %= T + X, lambda h,s: s[2], None, lambda h,s: s[1]

X %= pipe + T + X, lambda h,s: s[3], None, None, lambda h,s: UnionNode(h[0],s[2])                            
X %= G.Epsilon, lambda h,s: h[0]

T %= F + Y, lambda h,s: s[2], None, lambda h,s: s[1]  

Y %= F + Y, lambda h,s: s[2], None, lambda h,s: ConcatNode(h[0],s[1])                            
Y %= G.Epsilon, lambda h,s: h[0] 

F %= A + Z, lambda h,s: s[2], None, lambda h,s: s[1]

Z %= star, lambda h,s: ClosureNode(h[0]), None
Z %= G.Epsilon, lambda h,s: h[0]

A %= symbol, lambda h,s: SymbolNode(s[1]), None  
A %= epsilon, lambda h,s: EpsilonNode(s[1]), None                                                  
A %= opar + E + cpar, lambda h,s: s[2], None, None, None 


def regex_tokenizer(text, G, skip_whitespaces=True):
    tokens = []    
    fixed_tokens = { lex: Token(lex, G[lex]) for lex in '| * ( ) ε'.split() }
    special_char = False
    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        elif special_char:
            token = Token(char, G['symbol'])
            special_char = False            
        elif char == '\\':
            special_char = True
            continue 
        else:
            try:
                token = fixed_tokens[char]
            except:
                token = Token(char, G['symbol'])
        tokens.append(token)        
    tokens.append(Token('$', G.EOF))
    return tokens



parser = metodo_predictivo_no_recursivo(G)

def regex_automaton(regex):
    regex_tokens = regex_tokenizer(regex,G)
    regex_parser = parser(regex_tokens)
    regex_ast = evaluate_parse(regex_parser,regex_tokens)
    regex_nfa = regex_ast.evaluate()
    return automata_minimization(nfa_to_dfa(regex_nfa))

class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()    
    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):            
            automaton = regex_automaton(regex)           #
            automaton = State.from_nfa(automaton)   
            for state in automaton:
                if state.final:
                    state.tag = (token_type,n)
            regexs.append(automaton)
        return regexs    
    def _build_automaton(self):
        start = State('start')
        # Your code here!!!
        for automaton in self.regexs:
            start.add_epsilon_transition(automaton) 
        return start.to_deterministic()       
    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''        
        for symbol in string:
            # Your code here!!!         
            try:
                state = state[symbol][0] 
                lex = lex + symbol
            except TypeError:
                break       
        final = state                    
        final.tag = (None, float('inf'))
        for state in final.state:
            if state.final and state.tag[1] < final.tag[1]:
                final.tag = state.tag
        final_lex = lex          
        return final, final_lex    
    def _tokenize(self, text: str, skip_whitespaces=True):
        # Your code here!!!
        remaining_text = text
        while True:
            if skip_whitespaces and remaining_text[0].isspace():     # LINEAS AGREGADAS !!!!!!!!!!!!
                remaining_text = remaining_text[1:]
                continue                
            final_state, final_lex = self._walk(remaining_text)
            if final_lex == '':
                yield text.rsplit(remaining_text)[0], final_state.tag[0]
                return            
            yield final_lex, final_state.tag[0] 
            remaining_text = remaining_text.replace(final_lex,'',1)
            if remaining_text == '':
                break        
        yield '$', self.eof    
    def __call__(self, text, skip_whitespaces=True):
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text, skip_whitespaces) ]

nonzero_digits = '|'.join(str(n) for n in range(1,10))
letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))

lexer = Lexer([
    ('num', f'({nonzero_digits})(0|{nonzero_digits})*'),
    ('plus', '+'),
    ('minus', '-'),
    ('star', '\*'),
    ('div', '/'),
    ('pow', '^'),
    ('opar', '\('),
    ('cpar', '\)'),
    ('comma', ','),
    ('equals', '='),
    ('let' , 'let'),
    ('in' , 'in'),        
    ('id', f'({letters})({letters}|0|{nonzero_digits})*')
], 'eof')


text = 'let    x=10,y=222 in (332823948*xiom304230)'
print(f'\n>>> Tokenizando: "{text}"')
tokens = lexer(text)
print(tokens)