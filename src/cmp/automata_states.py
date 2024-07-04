from utils import DisjointSet, ContainerSet

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

        
class DFA(NFA):
    
    def __init__(self, states, finals, transitions, start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
        
    def _move(self, symbol):
        # Your code here
        self.current = self.transitions[self.current][symbol][0]
    
    def _reset(self):
        self.current = self.start
        
    def recognize(self, string):
        # Your code here
        for symbol in string:
            if symbol not in self.transitions[self.current]: return False
            self._move(symbol)
            
        recognized = self.current in self.finals
        self._reset()
        return recognized

def move(automaton, states, symbol):
    moves = set()
    for state in states:
        # Your code here
        mov = automaton.transitions[state]
        if symbol in mov.keys():
            for _state in mov[symbol]:
                moves.add(_state)
    
    return moves

def epsilon_closure(automaton, states):
    pending = [ s for s in states ] # equivalente a list(states) pero me gusta así :p
    closure = { s for s in states } # equivalente a  set(states) pero me gusta así :p
    
    while pending:
        state = pending.pop()
        # Your code here
        epsilon_trans = automaton.epsilon_transitions(state)
        for state in epsilon_trans:
            # La clausura tiene todos los estados visitados
            if state in closure: continue
            closure.add(state)
            pending.append(state)
                
    return ContainerSet(*closure)


def nfa_to_dfa(automaton):
    transitions = {}
    
    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [ start ]

    pending = [ start ]
    while pending:
        state = pending.pop()
        
        for symbol in automaton.vocabulary:
            # Your code here
            # ...
            
            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                # Your code here
                symbol_clousure = move(automaton, state, symbol)
                symbol_clousure = epsilon_closure(automaton, symbol_clousure)
                
                #no hacer nada si el simbolo no lleva a ninguna parte
                if(symbol_clousure == ContainerSet()): continue
                
                #si ya fue descubierto el estado, dejar solo la transicion
                founded = False
                for _state in states:
                    if _state.set == symbol_clousure.set:
                        transitions[state.id, symbol] = _state.id
                        founded = True
                        break
                if founded: continue
                
                #Es un estado nuevo
                symbol_clousure.id = len(states)
                symbol_clousure.is_final = any(s in automaton.finals for s in symbol_clousure)
                
                states.append(symbol_clousure)
                pending.append(symbol_clousure)
                
                transitions[state.id, symbol] = symbol_clousure.id
                
    finals = [ state.id for state in states if state.is_final ]
    dfa = DFA(len(states), finals, transitions)
    
    return dfa

#Automata minimization
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