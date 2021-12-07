def op_EBEHAV(state: State) -> None:            
    state.require(state.in_behaviour, 'Not inside any behaviour.', 'Try defining new behaviours using BEHAV.')
    state.require(
        not state.in_action, 
        'Cannot end behaviours inside actions.', 
        'Try ending current action using EACTION.'
    )
    
    state.in_behaviour = False
