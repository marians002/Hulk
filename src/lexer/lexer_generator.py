import sys
sys.path.append('/home/marian/Documents/MATCOM/Compilación/Hulk Repo/Hulk/')
from cmp.utils import Token
from cmp.automata import State
from lexer.regex import Regex


class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regex(table)
        self.automaton = self._build_automaton()

    def _build_regex(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            automaton = Regex(regex).automaton
            automaton = State.from_nfa(automaton)
            for state in automaton:
                if state.final:
                    state.tag = (n, token_type)
            regexs.append(automaton)
        return regexs

    def _build_automaton(self):
        start = State('start')
        for automaton in self.regexs:
            start.add_epsilon_transition(automaton)
        return start.to_deterministic()

    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''

        for symbol in string:
            lex += symbol
            try:
                state = state.get(symbol)
                if state.final:
                    final = state
                    final_lex = lex
            except KeyError:
                break

        return final, final_lex

    def _tokenize(self, text):
        (row, column) = (1, 1)
        while text:
            final_state, lex = self._walk(text)
            assert len(lex) != 0, 'Error'

            priority = [state.tag for state in final_state.state if state.tag]
            priority.sort()
            idx, token_type = priority[0]

            text = text[len(lex):]
            match lex:
                case '\n':
                    (row, column) = (row + 1, 1)
                case '\t':
                    (row, column) = (row, column + 4)
                case ' ':
                    (row, column) = (row, column + 1)
                case _:
                    yield lex, token_type, (row, column)
                    (row, column) = (row, column + len(lex))

        yield '$', self.eof, (row, column)

    def __call__(self, text):
        return [Token(lex, token_type, pos) for lex, token_type, pos in self._tokenize(text)]
