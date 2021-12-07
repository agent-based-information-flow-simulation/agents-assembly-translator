def op_MESSAGE(state: State, msg_type: str, msg_performative) -> None:
    state.require(not state.in_message, 'Already inside a message.', 'First end current message using EMESSAGE.')
    state.require(not state.in_agent, 'Cannot define messages inside agents.', 'First end current agent using EAGENT.')
    state.require(
        not state.message_exists(msg_type, msg_performative), 
        f'Message {msg_type}/{msg_performative} already exists in the current environment.'
    )
    state.require(
        is_valid_name(msg_type), 
        f'{msg_type} is not a correct name.', 
        f'Names can only contain alphanumeric signs, underscores and cannot be: {print_invalid_names()}.'
    )
    state.require(
        is_valid_name(msg_performative), 
        f'{msg_performative} is not a correct name.', 
        f'Names can only contain alphanumeric signs, underscores and cannot be: {print_invalid_names()}.'
    )
    
    state.in_message = True
    state.add_message(Message(msg_type, msg_performative))