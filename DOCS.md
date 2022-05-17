# Agents Assembly

## Type annotation definitions

`{...}` - One of the options from the brackets needs to be chosen, written as specified within the brackets.

`[...]` - Optional arguments.

`Name` - A unique sequence of alphanumeric characters which does not contain any forbidden symbols and does not begin with a number. Some instructions put further restrictions on `Name`s.

`Float` - A floating-point number or variable.

`MutFloat` - A floating-point variable with the possibility of being modified.

`Integer` - An integer. If a `Float` is passed as an argument of this type, it will be rounded down.

`Enum` - An enumerable that stores a state in the form of `EnumVal`.

`EnumVal` - A distinct enumerable state.

`Message` - A message defined using the `MESSAGE` instruction.

`Jid` - Agent identifier.

`ACLPerformative` - One of the FIPA-defined ACL performative types.

`DistArgs` - Arguments for a specified distribution. Mathematical constraints apply.

## Preprocessor
Preprocessor directives begin with `%`.

### Makros
Makros can be used to reduce repetitive code or improve readability. When called, they expand in-place the definition by substituting makro arguments for call parameters.

*Example usage:*
```aasm
%MAKRO add_if_greater_else val1, val2, flag
  SET flag, 0
  IGT val1, val2
    ADD val1, 1
    SET flag, 1
  EBLOCK
  ILTEQ val1, val2
    IEQ flag, 1
      ADD val2, 1
    EBLOCK
  EBLOCK
%EMAKRO

# ...omitted

ACTION hello, modify_self
  DECL flag, float 0
  add_if_greater_else param1, param2, flag
EACTION
```
### Constants
They are used to define globally set numbers. They can be used in all scopes (including agent and message params and network definition).

*Example usage:*
```aasm
%CONST sim_size, 10000

# ...omitted

AGENT manager
  PRM alive, float, init, sim_size
EAGENT
```

## Scope Modifiers

`GRAPH type: {statistical}` - Enters the scope for creation of a graph of specified `type`.

`EGRAPH` - Exists graph scope. It has to correspond to `GRAPH`.

*Example usage:*
```aasm
GRAPH statistical
  # graph definition
EGRAPH
```

`ACTION name: Name, type: {modify_self, send_msg}` - Enters scope for describing an Action of the specified `type`. The name is required to be unique within the `BEHAV` scope. It can only be used within the `BEHAV` scope.

`EACTION` - Exists action scope. It has to correspond to `ACTION`.

*Example usage:*
```aasm
ACTION add_friend, modify_self
  # action definition
EACTION
```

`BEHAV name: Name, type: {setup, one_time, cyclic, msg_rcv} [, b_args]` - Enters scope for describing a Behaviour of specified `type`. `b_args` depend on the specified `type`. The name is required to be unique within `AGENT` scope. It can only be used within `AGENT` scope.

Behavior types:
 * `setup` - Fires on setup, no additional arguments are used.
 * `one_time` (`b_args` is `delay: Float`) - Fires after `delay` seconds. `delay` must be greater than `0`.
 * `cyclic` (`b_args` is `period: Float`) - Fires every `period` seconds. `period` must be greater than `0`.
 * `msg_rcv` (`b_args` is `msg_name: Name, msg_type: ACLPerformative`) - Fires upon receiving message matching name `msg_name` and `msg_type`.

`EBEHAV` - Exists behavior scope. It has to correspond to `BEHAV`.

*Example usage:*
```aasm
BEHAV read_message, msg_rcv, test_message, inform
  # behavior definition
EBEHAV
```

`MESSAGE name: Name, performative: ACLPerformative` - Enters the scope for describing a Message of the specified name and performative.

`EMESSAGE` - Exists message scope. It has to correspond to `MESSAGE`.

*Example usage:*
```aasm
MESSAGE test_message, inform
  # message definition
EMESSAGE
```

`AGENT name: Name` - Enters the scope for describing an agent.

`EAGENT` - Exists agent scope. It has to correspond to `AGENT`.

*Example usage:*
```aasm
AGENT
  # agent definition here
EAGENT
```

## Message Scope
`PRM name: Name, type: {float}` - Creates a new message parameter of specified type. `name` cannot be `sender`, `type`, `performative`.

## Agent Scope
`PRM name: Name, type: {float, enum, list}, subtype: {init, dist, conn, msg} [, p_args]` - Creates an agent parameter of specified type and subtype. Describes the initial state of an agent by passing arguments `p_args`.

Types:
 * `float`
   * `init` (`p_args` is `val: Float`) - Creates a float parameter. Value `name` is set to `val` during agent initiation.
   * `dist` (`p_args` is `dist: {normal, uniform, exp}, dist_args: DistArgs`) - Creates a float parameter. Value `name` is set to a value drawn from specified `dist` distribution.
 * `enum` (`p_args` is `val1, val1%, ..., valn, valn%`) - Creates an enum parameter. Value `name` is set to one of `[val1, ... ,valn]`. Corresponding `vali%` arguments specify the percentage of the total agent population to have a specific value set on startup.
 * `list`
   * `conn` - Creates a connection list parameter. List is empty on startup.
   * `msg` - Creates a message list parameter. List is empty on startup.

## Action Scope: modifiers

`DECL name: Name, type: {float, conn} value: Float/Jid` - Creates a variable of specified `type` with `name` and `value`. The new variable can only be used in given action's scope.

`SET dst: MutFloat/Enum, value: Float/EnumVal` - Sets value of `dst` to `value`.

`SUBS dst: List, src: List, num: Integer` - Chooses `num` elements from `src` and sets `dst` to them.

## Action Scope: math expressions

`ADD dst: MutFloat, arg: Float` - Adds `arg` to `dst` and stores result in `dst`.

`MULT dst: MutFloat, arg: Float` - Multiplies `arg` by `dst` and stores result in `dst`.

`SUBT dst: MutFloat, arg: Float` - Subtracts `arg` from `dst` and stores result in `dst`.

`DIV dst: MutFloat, arg: Float` - Divides `arg` by `dst` and stores result in `dst`. If `arg` is `0` then the `ACTION` will finish early.

`SIN dst: MutFloat, arg: Float` - Calculates the sine of `arg` radians and stores it in `dst`.

`COS dst: MutFloat, arg: Float` - Calculates the cosine of `arg` radians and stores it in `dst`.

`POW dst: MutFloat, base: Float, arg: Float` - Calculates `base` raised to `arg` power and stores result in `dst`.

`LOG dst: MutFloat, base: Float, arg: Float` - Calculcates `base` logarithm of `arg` and stores result in `dst`.

## Action Scope: conditionals
`IEQ a: Float/Enum, b: Float/EnumVal` - Begins conditional block if `a` is equal to `b`. Needs matching `EBLOCK`.

`INEQ a: Float/Enum, b: Float/EnumVal` - Begins conditional block if `a` is not equal to `b`. Needs matching `EBLOCK`.

`ILT a: Float, b: Float` - Begins conditional block if `a` is less than `b`. Needs matching `EBLOCK`.

`IGT a: Float, b: Float` - Begins conditional block if `a` is greater than `b`. Needs matching `EBLOCK`.

`ILTEQ a: Float, b: Float` - Begins conditional block if `a` is less or equal `b`. Needs matching `EBLOCK`.

`IGTEQ a: Float, b: Float` - Begins conditional block if `a` is greater or equal `b`. Needs matching `EBLOCK`.

## Action Scope: loops
`WEQ a: Float/Enum, b: Float/EnumVal` - Begins loop block if `a` is equal to `b`. Needs matching `EBLOCK`.

`WNEQ a: Float/Enum, b: Float/EnumVal` - Begins loop block if `a` is not equal to `b`. Needs matching `EBLOCK`.

`WLT a: Float, b: Float` - Begins loop block if `a` is less than `b`. Needs matching `EBLOCK`.

`WGT a: Float, b: Float` - Begins loop block if `a` is greater than `b`. Needs matching `EBLOCK`.

`WLTEQ a: Float, b: Float` - Begins loop block if `a` is less or equal `b`. Needs matching `EBLOCK`.

`WGTEQ a: Float, b: Float` - Begins loop block if `a` is greater or equal `b`. Needs matching `EBLOCK`.

## Action scope: lists

`ADDE list: List, value: Message/Jid` - Adds `value` to `list`.

`REME list: List, value: Message/Jid` - Removes `value` from `list`. If `value` is not in the list, does nothing.

`REMEN list: List, num, Integer` - Removes `num` random elements from `list`. If `list` is too short, it clears it.

`LEN result: MutFlost, list: List` - Saves length of `list` in `result`.

`CLR list: List` - Clears contents of `list`.

`IN list: List, value: Message/Jid` - Begins conditional block if `val` is in `list`. Needs matching `EBLOCK`.

`NIN list: List, value: Message/Jid` - Begins conditional block if `val` is not in `list`. Needs matching `EBLOCK`.

`SUBS dst: List, src: List, num: Float` - Takes `num` randomly selected elements of `src` and stores them in `dst`.

`LW dst: List, val: Float/Jid, idx: Float` - Writes `val` at index `idx` of `dst`.

`LR dst: Float/Jid, src: List, idx: Float` - Reads value from list `src` at index `idx` and stores it in `dst`.

## Action scope: special

`EBLOCK` - Ends current conditional or loop block.

`SEND rcv: ConnList/Jid` - Sends message to `rcv`. Can only be used inside `send_msg` actions.

`RAND result: MutFloat, cast: {float, int}, dist: {uniform, normal, exp}, dist_args: DistArgs` - Stores a value drawn from specified `dist` distribution, casts it to `cast` type and stores it in `result`.

`.` (`msg.prm`) - Allows to access the value of `prm` from `msg`.
