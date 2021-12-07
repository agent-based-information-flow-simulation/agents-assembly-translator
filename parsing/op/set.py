def op_SET(state: State, arg1: str, arg2: str) -> None:
    state.require(state.in_action, 'Not inside any action.', f'SET can be used inside actions.')
    lhs = Argument(state, arg1)
    rhs = Argument(state, arg2)
    state.require(
        lhs.assignment_context(rhs), 
        'Mismatched types in the assignment context.', 
        f'ARG1 {lhs.explain()}, ARG2 {rhs.explain()}'
    )    
    
    state.last_action.add_instruction(Set(lhs, rhs))
