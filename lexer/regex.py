from lexer.automata import *
from cmp.ast import *
from cmp.pycompiler import Grammar
from cmp.utils import Token
from parser.LR1_parser_generator import LR1Parser
from cmp.evaluation import evaluate_reverse_parse


class EpsilonNode(AtomicNode):
    def evaluate(self):
        return NFA(states=1, finals=[0], transitions={})
    
class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        return NFA(states=2, finals=[1], transitions={(0, s): [1]})    
    
class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):        
        return NFA.automata_union(lvalue,rvalue)

class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):        
        return NFA.automata_concatenation(lvalue,rvalue)
    
class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value: NFA):        
        return value.automata_closure()

class PositiveClosureNode(UnaryNode):
    @staticmethod
    def operate(value: NFA):        
        return NFA.automata_concatenation(value,value.automata_closure())
    
class ZeroOrOneNode(UnaryNode):
    @staticmethod
    def operate(value: NFA):        
        return NFA.automata_union(value,EpsilonNode(G.EOF).evaluate())
    
class CharClassNode(Node):
    def __init__(self, symbols: list[SymbolNode]) -> None:
        self.symbols = symbols

    def evaluate(self):
        value = self.symbols[0].evaluate()  
        for symbol in self.symbols[1:]:            
            value = value.automata_union(symbol.evaluate())  
        return value

class RangeNode(Node):
    def __init__(self, first: SymbolNode, last: SymbolNode) -> None:
        self.first = first
        self.last = last

    def evaluate(self):
        value = [self.first]
        for i in range(ord(self.first.lex)+1,ord(self.last.lex)):
            value.append(SymbolNode(chr(i)))
        value.append(self.last)
        return value      
          
    


G = Grammar()

E = G.NonTerminal('E', True)
T, F, A, S = G.NonTerminals('T F A S')
pipe, star, plus, minus, quest, opar, cpar, obrack, cbrack, symbol, epsilon = G.Terminals('| * + - ? ( ) [ ] symbol ε')


E %= T, lambda h,s: s[1]
E %= E + pipe + T, lambda h,s: UnionNode(s[1],s[3])

T %= F, lambda h,s: s[1]
T %= T + F, lambda h,s: ConcatNode(s[1],s[2])

F %= A, lambda h,s: s[1]
F %= A + star, lambda h,s: ClosureNode(s[1])
F %= A + plus, lambda h,s: PositiveClosureNode(s[1])
F %= A + quest, lambda h,s: ZeroOrOneNode(s[1])

A %= symbol, lambda h,s: SymbolNode(s[1])
A %= epsilon, lambda h,s: EpsilonNode(s[1])                                                
A %= opar + E + cpar, lambda h,s: s[2]
A %= obrack + S + cbrack, lambda h,s: CharClassNode(s[2])

S %= symbol, lambda h,s: [SymbolNode(s[1])]
S %= symbol + S, lambda h,s: [SymbolNode(s[1])] + s[2]
S %= symbol + minus + symbol, lambda h,s: RangeNode(SymbolNode(s[1]),SymbolNode(s[3])).evaluate()
S %= symbol + minus + symbol + S, lambda h,s: RangeNode(SymbolNode(s[1]),SymbolNode(s[3])).evaluate() + s[4]


regex_parser = LR1Parser(G)


class Regex:
    def __init__(self, text: str) -> None:
        self.text = text
        self.automaton = self._build_automaton()       


    def __call__(self, w: str) -> bool:
        return self.automaton.recognize(w) 


    def _tokenize_regex(self):
        tokens = []

        fixed_tokens = {lex: Token(lex,G[lex]) for lex in '| * + - ? ( ) [ ] symbol ε'.split()}
    
        char_class = escape = False    

        for char in self.text:

            if escape:
                tokens.append(Token(char, symbol))
                escape = False
                continue

            if char == ']':
                char_class = False            
            elif char_class:
                if char != '-':
                    tokens.append(Token(char, symbol))
                    continue
            elif char == '[':
                char_class = True
            elif char == '\\':
                escape = True
                continue
            
            try:
                token = fixed_tokens[char]
            except KeyError:
                token = Token(char, symbol)
            tokens.append(token)                 
            
        tokens.append(Token('$', G.EOF))
        return tokens
    
    
    def _build_automaton(self):
        tokens = self._tokenize_regex()     
        
        try:
            parse, operations = regex_parser([token.token_type for token in tokens],get_shift_reduce=True)
        except TypeError:
            print(tokens) 
            raise TypeError

        ast = evaluate_reverse_parse(parse,operations,tokens)
        nfa = ast.evaluate()
        dfa = nfa.to_dfa()
        return dfa.automata_minimization()