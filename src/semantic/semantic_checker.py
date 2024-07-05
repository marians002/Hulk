import sys
sys.path.append('/home/marian/Documents/MATCOM/Compilación/Hulk Repo/Hulk/')
from type_collector import *
from type_builder import *
from type_checker import *
from format_visitor import *
from src.cmp.grammar import *
from src.cmp.utils import Token, tokenizer
from src.parser.ParserLR1 import *
from src.cmp.evaluation import evaluate_reverse_parse

text = '''
type animal{
    xa:Number=12;
    xz:Number="Manolo \" manolin";
    xa:Number=13;
}
type perro inherits animal{
    xb:Number=12;
    dogi:animal=12;
    xc:miloco=12;
}

type perro{
    xd:Number=12;
}


type animal{
    xe:Number=12;
}

print(43);
'''
fixed_tokens = {t.Name: Token(t.Name, t) for t in G.terminals if t not in {identifier, number}}





if __name__ == '__main__':
    tokens = tokenize_text(text)


def pprint_tokens(tokens):
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


if __name__ == '__main__':  pprint_tokens(tokens)


def run_pipeline(G, text):
    print('=================== TEXT ======================')
    print(text)
    print('================== TOKENS =====================')
    tokens = tokenize_text(text)
    pprint_tokens(tokens)
    print('=================== PARSE =====================')
    parser = LR1Parser(G)
    parse, operations = parser([t.token_type for t in tokens], get_shift_reduce=True)
    print('\n'.join(repr(x) for x in parse))
    print('==================== AST ======================')
    ast = evaluate_reverse_parse(parse, operations, tokens)
    formatter = FormatVisitor()
    tree = formatter.visit(ast)
    print(tree)
    return ast


if __name__ == '__main__': ast = run_pipeline(G, text)

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
