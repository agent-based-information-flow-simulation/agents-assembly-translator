def op_DECL(state: State, name: str, value: str) -> None:            
    state.require(state.in_action, 'Cannot declare variables outside actions.')
    state.require(
        is_valid_name(name), 
        f'{name} is not a correct name.', 
        f'Names can only contain alphanumeric signs, underscores and cannot be: {print_invalid_names()}.'
    )
    state.require(not state.last_agent.param_exists(name), f'{name} is already defined in current agent.')
    state.require(
        not state.last_action.is_declaration_in_scope(name), 
        f'{name} is already declared in current action scope.'
    )
    lhs = Argument(state, name)
    rhs = Argument(state, value)
    state.require(
        lhs.declaration_context(rhs), 
        'Mismatched types in the declaration context.', 
        f'ARG1 {lhs.explain()}, ARG2 {rhs.explain()}'
    )
    
    state.last_action.add_declaration(Declaration(lhs, rhs))
