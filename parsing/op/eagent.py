def op_EAGENT(state: State) -> None:    
    state.require(state.in_agent, 'Not inside any agent.', 'Try defining new agents using AGENT.')
    state.require(
        not state.in_behaviour, 
        'Cannot end an agent inside a behaviour.', 
        'First end current behaviour using EBEHAV.'
    )
    
    state.in_agent = False