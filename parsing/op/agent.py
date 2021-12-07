def op_AGENT(state: State, name: str) -> None:    
    state.require(not state.in_agent, 'Already inside an agent.', 'First end current agent using EAGENT.')
    state.require(
        not state.in_message, 
        'Cannot define agents inside messages.', 
        'First end current message using EMESSAGE.'
    )
    state.require(not state.agent_exists(name), f'Agent {name} already exists in the current environment.')
    state.require(
        is_valid_name(name), 
        f'{name} is not a correct name.', 
        f'Names can only contain alphanumeric signs, underscores and cannot be: {print_invalid_names()}.'
    )
    
    state.in_agent = True
    state.add_agent(Agent(name))