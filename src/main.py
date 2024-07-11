import sys
sys.path.append('/home/marian/Documents/MATCOM/Compilación/Hulk Repo/Hulk/src/')
from semantic.type_collector import *
from semantic.type_builder import *
from semantic.scopes_filler import *
from semantic.type_inferer import *
from semantic.type_checker import *
from semantic.format_visitor import *
from cmp.grammar import *
from cmp.utils import Token
from parser.ParserLR1 import LR1Parser
from cmp.evaluation import evaluate_reverse_parse
from lexer.lexer_generator import Lexer
from lexer.hulk_tokens import HULK_TOKENS
from cmp.pycompiler import Grammar
from interpreter.hulk_interpreter import *

text_hulk = """ print(42); """


def run_pipeline(G, table, text):
    print('=================== TEXT ======================')
    print(text)

    print('================== TOKENIZING =====================')

    HulkLexer = Lexer(table, G.EOF)
    tokens = HulkLexer(text)

    print('=================== PARSING =====================')

    HulkParser = LR1Parser(G)
    tokens = [t for t in tokens if t.token_type not in ('comment',)]
    parse, operations = HulkParser(tokens, get_shift_reduce=True)
    # print('\n'.join(repr(x) for x in parse))
    print('==================== AST ======================')
    ast = evaluate_reverse_parse(parse, operations, tokens)

    print('============== COLLECTING TYPES ===============')
    errors = []
    collector = TypeCollector(errors)
    context, errors = collector.visit(ast)
    # print('Errors:', errors)
    # print('Context:')
    # print(context)
    # print(ast)

    print('=============== BUILDING TYPES ================')
    builder = TypeBuilder(context, errors)
    # print('AST type:', type(ast))
    context, errors = builder(ast)
    # print('Errors: [')
    # for error in errors:
    #     print('\t', error)
    # print(']')
    # print('Context:')
    # print(context)

    print('=============== FILLING SCOPES ================')
    filler = ScopesFiller(context, errors)
    scope = filler.visit(ast)
    errors = filler.errors
    # print('Errors: [')
    # for error in errors:
    #     print('\t', error)
    # print(']')

    scope.define_variable("PI", context.get_type("Number"))
    scope.define_variable("E", context.get_type("Number"))

    print('================== INFERING TYPES ==================')
    inferer = TypeInferer(context, errors)
    inferer.visit(ast)
    context, errors = inferer.context, inferer.errors

    # print('Errors: [')
    # for error in errors:
    #     print('\t', error)
    # print(']')

    print('================== CHECKING TYPES ==================')
    checker = TypeChecker(context, errors)
    context, errors = checker.visit(ast)    
    # print('Context:')
    # print(context)
    print('Errors: [')
    for error in errors:
        print('\t', error)
    print(']')
    

    print('================== AST INTERPRETER ==================')
    interpreter = Interpreter(context.types)
    value = interpreter.visit(ast)
    print(value)


if __name__ == '__main__': ast = run_pipeline(G, HULK_TOKENS, text_hulk)

