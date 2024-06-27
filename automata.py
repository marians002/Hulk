import pydot
from cmp.utils import ContainerSet
class NFA:
    def __init__(self, states, finals, transitions, start=0):
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions = { state: {} for state in range(states) }
        
        for (origin, symbol), destinations in transitions.items():
            assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)
            
        self.vocabulary.discard('')
        
    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()
            
    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        for (start, tran), destinations in self.map.items():
            tran = 'ε' if tran == '' else tran
            G.add_node(pydot.Node(start, shape='circle', style='bold' if start in self.finals else ''))
            for end in destinations:
                G.add_node(pydot.Node(end, shape='circle', style='bold' if end in self.finals else ''))
                G.add_edge(pydot.Edge(start, end, label=tran, labeldistance=2))

        G.add_edge(pydot.Edge('start', self.start, label='', style='dashed'))
        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass

class DFA(NFA):
    
    def __init__(self, states, finals, transitions, start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
        
    def _move(self, symbol):
        # Your code here
        try:
            self.current = self.transitions[self.current][symbol][0]
        except KeyError:
            self.current = None
    
    def _reset(self):
        self.current = self.start
        
    def recognize(self, string):
        # Your code here
        self._reset()
        for symbol in string:
            self._move(symbol)
        return self.current in self.finals

def move(automaton, states, symbol):
    moves = set()
    for state in states:
        # Your code here
        try:
            moves.update(automaton.map[(state,symbol)])
        except KeyError:
            pass
    return moves
def epsilon_closure(automaton, states):
    pending = [ s for s in states ] # equivalente a list(states) pero me gusta así :p
    closure = { s for s in states } # equivalente a  set(states) pero me gusta así :p
    
    while pending:
        state = pending.pop()
        
        # Your code here
        try:
            new_states = automaton.map[(state,'')]
            closure.update(new_states)
            closure.update(epsilon_closure(automaton,new_states).set)
        except KeyError:
            pass

    return ContainerSet(*closure)
def nfa_to_dfa(automaton):
    
    transitions = {}
    
    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [ start ]
    state_sets = [ start.set ]

    pending = [ start ]
    index = 0
    while pending:
        state = pending.pop()
        
        for symbol in automaton.vocabulary:
            # Your code here            
            next_state_set = epsilon_closure(automaton, move(automaton, list(state.set), symbol)).set

            if not next_state_set:    # Para obtener un automata completamente especificado
                continue              # comentar estas dos lineas
                        
            try:
                i = state_sets.index(next_state_set)
                next_state = states[i]
            except ValueError:                
                next_state = ContainerSet(*next_state_set)
                index += 1
                next_state.id = index
                next_state.is_final = any(s in automaton.finals for s in next_state)
                           
                states.append(next_state)
                state_sets.append(next_state_set)
                pending.append(next_state)          

            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                # Your code here
                transitions[state.id,symbol] = next_state.id
    
    finals = [ state.id for state in states if state.is_final ]
    dfa = DFA(len(states), finals, transitions)
    return dfa

def nfa_recognize(automaton: NFA, string: str):
    
    states = epsilon_closure(automaton, [automaton.start]).set
    
    while states and string:
        symbol = string[0]

        states = epsilon_closure(automaton, move(automaton, states, symbol)).set        
       
        string = string[1:]

    return len(states.intersection(automaton.finals)) > 0

def automata_union(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        ## Relocate a1 transitions ...
        # Your code here
        transitions[d1 + origin, symbol] = [d1 + d for d in destinations]

    for (origin, symbol), destinations in a2.map.items():        
        # Your code here
        transitions[d2 + origin, symbol] = [d2 + d for d in destinations]
    
    ## Add transitions from start state ...
    transitions[start, ''] = [d1,d2]
    
    ## Add transitions to final state ...
    transitions[d2 - 1, ''] = [final]
    transitions[final - 1, ''] = [final]
            
    states = a1.states + a2.states + 2
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def automata_concatenation(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 0
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        ## Relocate a1 transitions ...
        # Your code here
        transitions[origin, symbol] = destinations

    for (origin, symbol), destinations in a2.map.items():
        ## Relocate a2 transitions ...
        # Your code here
        transitions[d2 + origin, symbol] = [d2 + d for d in destinations]
    
    ## Add transitions to final state ...
    transitions[d2 - 1, ''] = [d2]
    transitions[final - 1, ''] = [final]
            
    states = a1.states + a2.states + 1
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def automata_closure(a1):
    transitions = {}
    
    start = 0
    d1 = 1
    final = a1.states + d1
    

    for (origin, symbol), destinations in a1.map.items():
        ## Relocate automaton transitions ...
        # Your code here
        transitions[d1 + origin, symbol] = [d1 + d for d in destinations]              
    
    ## Add transitions from start state ...
    # Your code here
    transitions[start, ''] = [d1]
    
    ## Add transitions to final state and to start state ...
    # Your code here
    transitions[final - 1, ''] = [final]
    transitions[final,''] = [start]  
            
    states = a1.states +  2
    finals = {start,final}
    
    return NFA(states, finals, transitions, start)

from cmp.utils import DisjointSet

dset = DisjointSet(*range(10))
print('> Inicializando conjuntos disjuntos:\n', dset)

dset.merge([5,9])
print('> Mezclando conjuntos 5 y 9:\n', dset)

dset.merge([8,0,2])
print('> Mezclando conjuntos 8, 0 y 2:\n', dset)

dset.merge([2,9])
print('> Mezclando conjuntos 2 y 9:\n', dset)

print('> Representantes:\n', dset.representatives)
print('> Grupos:\n', dset.groups)
print('> Nodos:\n', dset.nodes)
print('> Conjunto 0:\n', dset[0], '--->', type(dset[0]))
print('> Conjunto 0 [valor]:\n', dset[0].value, '--->' , type(dset[0].value))
print('> Conjunto 0 [representante]:\n', dset[0].representative, '--->' , type(dset[0].representative))

def distinguish_states(group, automaton, partition):
    split = {}
    vocabulary = tuple(automaton.vocabulary)

    for member in group:
        state = member.value

        # Your code here
        destinations = []
        for char in vocabulary:            
            destinations.append(partition[automaton.transitions[state][char][0]].representative)
        destinations = tuple(destinations)
        
        try:
            split[destinations].append(state)    
        except KeyError:
            split[destinations] = [state]     

    return [ group for group in split.values()]
            
def state_minimization(automaton):
    partition = DisjointSet(*range(automaton.states))
    
    ## partition = { NON-FINALS | FINALS }
    finals = automaton.finals
    non_finals = [state for state in range(automaton.states) if state not in finals]

    partition.merge(finals)
    partition.merge(non_finals)        


    while True:
        new_partition = DisjointSet(*range(automaton.states))
        
        ## Split each group if needed (use distinguish_states(group, automaton, partition))
        # Your code here
        for group in partition.groups:
            new_groups = distinguish_states(group,automaton,partition)

            for new_group in new_groups:                
                new_partition.merge(new_group)

        if len(new_partition) == len(partition):
            break

        partition = new_partition
        
    return partition

def automata_minimization(automaton):
    partition = state_minimization(automaton)
    
    states = [s.value for s in partition.representatives]
    
    transitions = {}
    for i, state in enumerate(states):
        ## origin = ???
        # Your code here
        origin = state

        for symbol, destinations in automaton.transitions[origin].items():
            # Your code here
            destination = destinations[0]
            new_destination = partition[destination].representative.value
            new_destination = states.index(new_destination)
            
            try:
                transitions[i,symbol]
                assert False
            except KeyError:
                # Your code here
                transitions[i,symbol] = new_destination
    
    ## finals = ???
    ## start  = ???
    # Your code here
    finals = [states.index(state) for state in states if state in automaton.finals]
    for group in partition.groups:
        for member in group:
            if automaton.start == member.value:
                start = states.index(partition[member.value].representative.value)  
                break         
    #start = [states.index(group[0].value) for group in partition.groups if automaton.start in group][0]
    
    return DFA(len(states), finals, transitions, start)