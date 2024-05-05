import regex
import re

'''
Grammar:

E => T
    | T + E
    | T - E
T => int
    | T * T
    | T / T
    |(E)
    
    5 + 3
    625 / 5
    6 - 3 * 8
    (3 + 5) * 10
    
Tokens: <id, type>

numbers : < %d , num >
open_p : < ( , open_p >
close_p : < ) , close_p >
binary operators : < + | - | * | div , b_op >


'''
class Token:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        
class Lexer:
    
    def __init__(self, program):
        self.next_token = 0
        self.Tokens = self.tokenizer(program)
        
    def tokenizer(self, program: str):
        # remove all blank spaces from program:
        
        Tokens = []
        
        while (self.next_token != program.__len__()):
            char = program[self.next_token]
        
    
        return Tokens
    
    