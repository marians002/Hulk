import sys
sys.path.append('/home/carlosbreso/Data/Code/Python/HulkCompiler/Hulk/src/')
from type_collector import *
from type_builder import *
from scopes_filler import *
from format_visitor import *
from cmp.grammar import *
from cmp.utils import Token
from parser.ParserLR1 import LR1Parser
from cmp.evaluation import evaluate_reverse_parse
from lexer.lexer_generator import Lexer
from lexer.hulk_tokens import HULK_TOKENS
from cmp.pycompiler import Grammar

text_hulk = """type Point(x,y) {
    x = x;
    y = y;

    getX() => self.x;
    getY() => self.y;

    setX(x: Number) => self.x := x;
    setY(y: Number) => self.y := y;
}

type PolarPoint inherits Point {
    rho() => sqrt(self.getX() ^ 2 + self.getY() ^ 2);
}

type Polar(phi, rho) inherits Point(rho * sin(phi), rho * cos(phi)) {
    rho() => sqrt(self.getX() ^ 2 + self.getY() ^ 2);
}

let pt = new Point(3,4) in {
    new Polar(1,2);
    print("x: " @ pt.getX() @ "; y: " @ pt.getY());
}


"""       



def run_pipeline(G, table, text):
    print('=================== TEXT ======================')
    print(text)

    print('================== TOKENS =====================')
    HulkLexer = Lexer(table, G.EOF)
    tokens = HulkLexer(text)
    # for t in tokens:
    #     print(t)
    print('=================== PARSE =====================') 
    HulkParser = LR1Parser(G)
    tokens = [t for t in tokens if t.token_type not in ('comment',)]
    parse, operations = HulkParser(tokens, get_shift_reduce=True)
    print('\n'.join(repr(x) for x in parse))
    print('==================== AST ======================')
    ast = evaluate_reverse_parse(parse, operations, tokens)
      
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
    print('=============== CHECKING TYPES ================')
    filler = ScopesFiller(context, errors)
    scope = filler.visit(ast)
    print('Errors: [')
    for error in errors:
        print('\t', error)
    print(']')
    return True


if __name__ == '__main__': ast = run_pipeline(G, HULK_TOKENS, text_hulk)

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
