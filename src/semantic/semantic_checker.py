import sys
sys.path.append('/home/carlosbreso/Data/Code/Python/HulkCompiler/Hulk/src')
from type_collector import *
from type_builder import *
from type_checker import *
from format_visitor import *
from cmp.grammar import *
from cmp.utils import Token, tokenizer
from parser.ParserLR1 import LR1Parser
from cmp.evaluation import evaluate_reverse_parse
from lexer.lexer_generator import Lexer
from lexer.hulk_tokens import HULK_TOKENS
from cmp.tools.parsing import LR1Parser as JParser
from cmp.pycompiler import Grammar
#from cmp.enemy_token_table import *


myTokens = [
        ("num", '(0|[1-9][0-9]*)(\.[0-9]+)?'),
        (";", ';')
    ]

test_grammar1 = '7;'
text_hulk = """ let a = 0 in {
    print(a);
    a := 1;
    print(a);
}; """



def run_pipeline(G, table, text):
    print('=================== TEXT ======================')
    print(text)
    print('================== TOKENS =====================')
    HulkLexer = Lexer(table, G.EOF)
    tokens = HulkLexer(text)
    for t in tokens:
        print(t)
    #ttypes = [t.token_type for t in tokens]
    print('=================== PARSE =====================') 
    HulkParser = LR1Parser(G)
    #HulkParser = JParser(G)
    tokens = [t for t in tokens if t.token_type not in ['comment','space', 'endofline']]
    parse, operations = HulkParser(tokens, get_shift_reduce=True)
    print('\n'.join(repr(x) for x in parse))
    print('==================== AST ======================')
    ast = evaluate_reverse_parse(parse, operations, tokens)
    formatter = FormatVisitor()
    tree = formatter.visit(ast)
    print(tree)
    return ast


if __name__ == '__main__': ast = run_pipeline(G, HULK_TOKENS, text_hulk)

deprecated_pipeline = run_pipeline


def run_pipeline(G, text):
    ast = deprecated_pipeline(G, text)
    print('============== COLLECTING TYPES ===============')
    errors = []
    collector = TypeCollector(errors)
    collector.visit(ast)
    context = collector.context
    print('Errors:', errors)
    print('Context:')
    print(context)
    print('=============== BUILDING TYPES ================')
    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    print('Errors: [')
    for error in errors:
        print('\t', error)
    print(']')
    print('Context:')
    print(context)
    return ast, errors, context
