def op_EMESSAGE(state: State) -> None:    
    state.require(state.in_message, 'Not inside any message.', 'Try defining new messages using MESSAGE.')
    
    state.in_message = False
    