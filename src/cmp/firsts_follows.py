from cmp.utils import ContainerSet


# Computes First(alpha), given First(Vt) and First(Vn) 
# alpha in (Vt U Vn)*
def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()

    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False

    ###################################################
    # alpha == epsilon ? First(alpha) = { epsilon }
    ###################################################
    if alpha_is_epsilon:
        first_alpha.set_epsilon()
        return first_alpha
    ###################################################

    for symbol in alpha:
        # First(Xi) subconjunto First(alpha)
        first_alpha.update(firsts[symbol])

        # epsilon pertenece a First(X1)...First(Xi) ? First(Xi+1) subconjunto de First(X) y First(alpha)
        if not firsts[symbol].contains_epsilon:
            break
    else:
        # epsilon pertenece a First(X1)...First(XN) ? epsilon pertence a First(X) y al First(alpha)
        first_alpha.set_epsilon()

    # First(alpha)
    return first_alpha


# Computes First(Vt) U First(Vn) U First(alpha)
# P: X -> alpha
def compute_firsts(G):
    firsts = {}
    change = True

    # init First(Vt)
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)

    # init First(Vn)
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()

    while change:
        change = False

        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right

            # get current First(X)
            first_X = firsts[X]

            # init First(alpha)
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()

            # CurrentFirst(alpha)???
            local_first = compute_local_first(firsts, alpha)

            # update First(X) and First(alpha) from CurrentFirst(alpha)
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)

    # First(Vt) + First(Vt) + First(RightSides)
    return firsts


# def compute_follows(G, firsts):
#     follows = {}
#     change = True

#     local_firsts = {}

#     # init Follow(Vn)
#     for nonterminal in G.nonTerminals:
#         follows[nonterminal] = ContainerSet()
#     follows[G.startSymbol] = ContainerSet(G.EOF)

#     while change:
#         change = False

#         # P: X -> alpha
#         for production in G.Productions:
#             X = production.Left
#             alpha = production.Right

#             follow_X = follows[X]

#             ###################################################
#             # X -> zeta Y beta
#             # First(beta) - { epsilon } subset of Follow(Y)
#             # beta ->* epsilon or X -> zeta Y ? Follow(X) subset of Follow(Y)
#             ###################################################
#             if alpha.IsEpsilon:
#                 continue

#             n = len(alpha._symbols) - 1
#             for i in range(n):
#                 Y = alpha._symbols[i]
#                 beta = alpha._symbols[i + 1]
#                 if Y.IsNonTerminal:
#                     change |= follows[Y].update(firsts[beta])
#                     if firsts[beta].contains_epsilon:
#                         change |= follows[Y].update(follow_X)
#                 if i == n - 1 and beta.IsNonTerminal:
#                     change |= follows[beta].update(follow_X)
#             ###################################################

#     # Follow(Vn)
#     return follows


# from itertools import islice

def compute_follows(G, firsts):
    follows = { }
    change = True
    
    local_firsts = {}
    
    # init Follow(Vn)
    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)
    
    while change:
        change = False
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            follow_X = follows[X]
            
            ###################################################
            # X -> zeta Y beta
            # First(beta) - { epsilon } subset of Follow(Y)
            # beta ->* epsilon or X -> zeta Y ? Follow(X) subset of Follow(Y)
            ###################################################

            for i in range (len(alpha)):
                if alpha[i].IsNonTerminal:
                    follow_Y = follows[alpha[i]]
                    
                    beta = alpha[i+1:] # lo que le sigue a la posicion actual
                    
                    if beta not in local_firsts:
                        local_firsts[beta] = compute_local_first(firsts, beta)
                    
                    first_beta = local_firsts[beta]
                    
                    change |= follow_Y.update(first_beta) 
                    
                    if first_beta.contains_epsilon:
                        # manejar caso de beta -> epsilon
                        change |= follow_Y.hard_update(follow_X)

    # Follow(Vn)
    return follows
