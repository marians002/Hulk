from cmp.utils import ContainerSet, DisjointSet


class NFA:
    def __init__(self, states: int, finals: list[int], transitions: dict[(int,str),list[int]], start: int = 0):
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
        
    def epsilon_transitions(self, state: int):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()
        

    def to_dfa(self):
        transitions = {}
    
        start = self._epsilon_closure([self.start])
        start.id = 0
        start.is_final = any(s in self.finals for s in start)
        states = [ start ]

        pending = [ start ]
        while pending:
            state = pending.pop()
        
            for symbol in self.vocabulary:

                next_state = self._epsilon_closure(self._move(state,symbol))

                if not next_state:
                    continue

                for item in states:
                    if item == next_state:
                        next_state = item
                        break
                else:
                    next_state.id = len(states)
                    next_state.is_final = any(state in self.finals for state in next_state)
                    states.append(next_state)
                    pending.append(next_state)


                try:
                    transitions[state.id, symbol]
                    assert False, 'Invalid DFA!!!'
                except KeyError:
                    transitions[state.id,symbol] = next_state.id          
      
        finals = [ state.id for state in states if state.is_final ]
        dfa = DFA(len(states), finals, transitions)
        return dfa
        

    def _move(self, states, symbol):
        moves = set()
        for state in states:
            try:
                moves.update(self.transitions[state][symbol]) 
            except:
                pass
        return moves

    def _epsilon_closure(self, states):
        pending = [ s for s in states ] 
        closure = { s for s in states }    

        while pending:
            state = pending.pop()
            next_states = self.epsilon_transitions(state)
            
            for item in next_states:
                if item not in pending:
                    pending.append(item)
            closure.update(next_states)
                
        return ContainerSet(*closure)
    


    def automata_union(a1, a2):
        transitions = {}
    
        start = 0
        d1 = 1
        d2 = a1.states + d1
        final = a2.states + d2
    
        for (origin, symbol), destinations in a1.map.items():
            ## Relocate a1 transitions ...
            transitions[d1 + origin, symbol] = [d1 + d for d in destinations]

        for (origin, symbol), destinations in a2.map.items():
            ## Relocate a2 transitions ...
            transitions[d2 + origin, symbol] = [d2 + d for d in destinations]
    
        ## Add transitions from start state ...
        transitions[start, ''] = [a1.start + d1, a2.start + d2]
    
        ## Add transitions to final state ...
        for i in a1.finals:
            try:
                transitions[i + d1, ''].add(final)
            except KeyError:
                transitions[i + d1, ''] = [final]
        for i in a2.finals:
            try:
                transitions[i + d2, ''].add(final)
            except KeyError:
                transitions[i + d2, ''] = [final]
            
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
            transitions[origin, symbol] = destinations

        for (origin, symbol), destinations in a2.map.items():
            ## Relocate a2 transitions ...
            transitions[d2 + origin, symbol] = [d2 + d for d in destinations]
        
        ## Add transitions to final state ...
        for i in a1.finals:
            try:
                transitions[i + d1, ''].add(a2.start + d2)
            except KeyError:
                transitions[i + d1, ''] = [a2.start + d2]
        for i in a2.finals:
            try:
                transitions[i + d2, ''].add(final)
            except KeyError:
                transitions[i + d2, ''] = [final]
                
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
            transitions[d1 + origin, symbol] = [d1 + d for d in destinations] 
        
        ## Add transitions from start state ...
        transitions[start, ''] = [a1.start + d1 , final]
        
        ## Add transitions to final state and to start state ...
        for i in a1.finals:
            try:
                transitions[i + d1, ''].add(final)
                transitions[i + d1, ''].add(a1.start + d1)
            except KeyError:
                transitions[i + d1, ''] = [final, a1.start + d1]
                
        states = a1.states +  2
        finals = { final }
        
        return NFA(states, finals, transitions, start)
    


class DFA(NFA):    
    def __init__(self, states: int, finals: list[int], transitions: dict[(int,str):int], start: int = 0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
        
    def _move(self, symbol: str) -> bool:
        try:
            self.current = self.transitions[self.current][symbol][0]
            return True
        except KeyError:
            return False
    
    def _reset(self):
        self.current = self.start
        
    def recognize(self, string: str) -> bool:
        self._reset()
        for symbol in string:
            if not self._move(symbol):
                return False
        return self.current in self.finals
    

    def automata_minimization(automaton):
        partition = DFA.state_minimization(automaton)
        
        states = [s for s in partition.representatives]
        
        transitions = {}
        for i, state in enumerate(states):
            origin = state.value
            for symbol, destinations in automaton.transitions[origin].items():            
                new_destination = states.index(partition[destinations[0]].representative)

                try:
                    transitions[i,symbol]
                    assert False
                except KeyError:
                    transitions[i,symbol] = new_destination
        
        start = states.index(partition[automaton.start].representative)
        finals = set([i for i in range(len(states)) if states[i].value in automaton.finals])
        
        return DFA(len(states), finals, transitions, start) 
    

    def state_minimization(automaton):
        partition = DisjointSet(*range(automaton.states))
        
        finals = automaton.finals
        non_finals = [state for state in range(automaton.states) if state not in finals]
        partition.merge(finals)
        partition.merge(non_finals)
        
        while True:
            new_partition = DisjointSet(*range(automaton.states))
            
            for group in partition.groups:
                new_groups = DFA.distinguish_states(group,automaton,partition)
                for new_group in new_groups:                
                    new_partition.merge(new_group)        

            if len(new_partition) == len(partition):
                break

            partition = new_partition
            
        return partition
    
    @staticmethod
    def distinguish_states(group, automaton, partition):        
        split = {}
        vocabulary = tuple(automaton.vocabulary)
        
        transition = automaton.transitions

        for member in group:
            for item in split.keys():
                for symbol in vocabulary:
                    q1 = None
                    q2 = None
                    try:
                        q1 = partition[transition[item][symbol][0]].representative
                    except KeyError:
                        q1 = None
                    try:
                        q2 = partition[transition[member.value][symbol][0]].representative
                    except KeyError:
                        q2 = None
                    if q1 != q2:
                        break
                else:
                    split[item].append(member.value)
                    break
            else:
                split[member.value] = [member.value]
                        

        return [ group for group in split.values()]
    
    
    
    


    











            


