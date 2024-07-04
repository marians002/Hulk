import sys

sys.path.append('/home/carlosbreso/Data/Code/Python/HulkCompiler/Hulk/src')
# para importar tienes que definir la ruta de donde estan los modulos
from cmp.pycompiler import Grammar, Item
from cmp.utils import ContainerSet
from cmp.automata import State, multiline_formatter
from cmp.firsts_follows import compute_local_first, compute_firsts
from cmp.grammar import *


class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()

    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w, get_shift_reduce=False):
        stack = [0]
        cursor = 0
        output = []
        operations = []

        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose:
                print(stack, '<---||--->', w[cursor:])

            # (Detect error)

            action, tag = self.action[state, lookahead]
            # (Shift case)
            match action:
                case self.SHIFT:
                    stack.append(lookahead)
                    stack.append(tag)
                    operations.append(self.SHIFT)
                    cursor += 1
                # (Reduce case)
                case self.REDUCE:
                    production = self.G.Productions[tag]
                    X, beta = production
                    for i in range(2 * len(beta)):
                        stack.pop()
                    l = stack[-1]
                    stack.append(X.Name)
                    stack.append(self.goto[l, X])
                    output.append(production)
                    operations.append(self.REDUCE)
                # (OK case)
                case self.OK:
                    break
                # (Invalid case)
                case _:
                    raise Exception
        if not get_shift_reduce:
            return output
        else:
            return output, operations


def expand(G, item, firsts):
    """ Expande un no terminal, obteniendo sus producciones tales que
    el lookahead pertenezca al first de lo que habia en la produccion a
    partir de la que se expandio concatenado su lookahead """

    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []

    lookaheads = ContainerSet()
    
    # Compute lookahead for child items
    for preview in item.Preview():
        lookaheads.update(compute_local_first(firsts, preview))

    assert not lookaheads.contains_epsilon
    # Build and return child items
    output = []
    for production in G.Productions:
        if production.Left == next_symbol:
            output.append(Item(production,0,lookaheads))
    return output


def compress(items):
    """ Combina items iguales que tienen center distinto"""
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)

    return {Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items()}


def closure_lr1(G, items, firsts):
    """ Clausura de un item, equivalente a la epsilon clausura de un estado """
    closure = ContainerSet(*items)
    
    changed = True
    while changed:
        changed = False
        
        new_items = ContainerSet()
        for item in closure:
            for new_item in expand(G, item, firsts):
                new_items.add(new_item)            

        
        changed = closure.update(new_items)
        
    return compress(closure)


def goto_lr1(G, items, symbol, firsts=None, just_kernel=False):
    """ Transiciones en el automata LR1 """
    
    assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(G, items, firsts)


def build_LR1_automaton(G):
    """ Automata necesario para construir la tabla """

    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])

    closure = closure_lr1(G, start, firsts)
    automaton = State(frozenset(closure), True)
    pending = [start]
    visited = {start: automaton}

    while pending:
        current = pending.pop()
        current_state  = visited[current]
        
        for symbol in G.terminals + G.nonTerminals:
            # Get/Build `next_state`
            goto_set = frozenset(goto_lr1(G, current_state.state, symbol, firsts))
            if not goto_set:
                continue
                
            if goto_set in visited:
                next_state = visited[goto_set]
            else:
                pending.append(goto_set)
                visited[goto_set] = next_state = State(goto_set, True)
                   
            current_state.add_transition(symbol.Name, next_state)

    automaton.set_formatter(multiline_formatter)
    return automaton


class LR1Parser(ShiftReduceParser):

    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)

        automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose:
                print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:
                # Fill `self.Action` and `self.Goto` according to `item`
                X = item.production.Left

                symbol = item.NextSymbol

                if X == G.startSymbol and item.IsReduceItem:
                    self._register(self.action, (idx, G.EOF), (self.OK, 0))

                elif item.IsReduceItem:
                    k = self.G.Productions.index(item.production)
                    for s in item.lookaheads:
                        self._register(self.action, (idx, s), (self.REDUCE, k))

                elif symbol.IsTerminal:
                    self._register(self.action, (idx, symbol), (self.SHIFT, node.transitions[symbol.Name][0].idx))

                else:
                    self._register(self.goto, (idx, symbol), node.transitions[symbol.Name][0].idx)

    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value
