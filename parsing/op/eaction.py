def op_EACTION(state: State) -> None:            
    state.require(state.in_action, 'Not inside any action.', 'Try defining new actions using ACTION.')
    state.require(
        state.last_action._nested_blocks_count == 0, 
        'There are unclosed blocks.', 
        'Try closing them using EBLOCK.'
    )
    
    state.in_action = False
