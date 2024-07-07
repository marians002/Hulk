import sys
sys.path.append('/home/marian/Documents/MATCOM/Compilación/Hulk Repo/Hulk/src/')
from type_collector import *
from type_builder import *
from scopes_filler import *
from format_visitor import *
from cmp.grammar import *
from cmp.utils import Token, tokenizer
from parser.ParserLR1 import LR1Parser
from cmp.evaluation import evaluate_reverse_parse
from lexer.lexer_generator import Lexer
from lexer.hulk_tokens import HULK_TOKENS
# from cmp.tools.parsing import LR1Parser as JParser

text = '42;'

""" fixed_tokens = {t.Name: Token(t.Name, t) for t in G.terminals if t not in {identifier, number}}


@tokenizer(G, fixed_tokens)
def tokenize_text(token):
    lex = token.lex
    try:
        float(lex)
        return token.transform_to(number)
    except ValueError:
        return token.transform_to(identifier)


if __name__ == '__main__':
    tokens = tokenize_text(text) """


""" def pprint_tokens(tokens):
    indent = 0
    pending = []
    for token in tokens:
        pending.append(token)
        if token.token_type in {ocur, ccur, semi}:
            if token.token_type == ccur:
                indent -= 1
            print('    ' * indent + ' '.join(str(t.token_type) for t in pending))
            pending.clear()
            if token.token_type == ocur:
                indent += 1
    print(' '.join([str(t.token_type) for t in pending]))


if __name__ == '__main__':  pprint_tokens(tokens) """


def run_pipeline(G, text):
    print('=================== TEXT ======================')
    # print(text)
    print('================== TOKENS =====================')
    HulkLexer = Lexer(HULK_TOKENS, G.EOF)
    tokens = HulkLexer(text)
    for t in tokens:
        print(t)
    #ttypes = [t.token_type for t in tokens]
    print('=================== PARSE =====================')
    HulkParser = LR1Parser(G)
    #HulkParser = JParser(G)
    parse, operations = HulkParser(tokens, get_shift_reduce=True)
    print('\n'.join(repr(x) for x in parse))
    print('==================== AST ======================')
    ast = evaluate_reverse_parse(parse, operations, tokens_test)
    
    return True


if __name__ == '__main__': ast = run_pipeline(G, text)

# deprecated_pipeline = run_pipeline


# def run_pipeline(G, text):
#     ast = deprecated_pipeline(G, text)
#     print('============== COLLECTING TYPES ===============')
#     errors = []
#     collector = TypeCollector(errors)
#     collector.visit(ast)
#     context = collector.context
#     print('Errors:', errors)
#     print('Context:')
#     print(context)
#     print('=============== BUILDING TYPES ================')
#     builder = TypeBuilder(context, errors)
#     builder.visit(ast)
#     print('Errors: [')
#     for error in errors:
#         print('\t', error)
#     print(']')
#     print('Context:')
#     print(context)
#     return ast, errors, context
