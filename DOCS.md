# Agents Assembly instructions

## How to use this documentation

`{...}` -

`Name` - 

`Float` -

`ACLPerformative`



## Scope Modifiers

`GRAPH` | **args:** `type: {statistical}` | Enters the scope for creation of a graph of specified `type`

`EGRAPH` | - | Exists graph scope. Has to correspond to `GRAPH`

*Example usage:*
```aasm
GRAPH statistical
#
# graph definition here
#
EGRAPH
```

`ACTION` | **args:** `name: Name, type: {modify_self, send_msg}` | Enters scope for describing an Action of the specified `type`. The name is required to be unique within `BEHAV` scope. It can only be used within `BEHAV` scope.

`EACTION` | - | Exists action scope. Has to correspond to `ACTION`

*Example usage:*
```aasm
ACTION add_friend, modify_self
#
# action definition here
#
EACTION
```

`BEHAV` | **args:** `name: Name, type: {setup, one_time, cyclic, msg_rcv}, b_args<sup>**</sup>` | Enters scope for describing a Behaviour of specified `type`. `b_args` depend on the specified `type`. The name is required to be unique within `AGENT` scope. It can only be used within `AGENT` scope.

`b_args:`
 * `setup`: | - | Fires on setup
 * `one_time`: | `delay: Float` | Fires after `delay` seconds. `delay` must be greater than `0`.
 * `cyclic`: | `cycle: Float` | Fires every `cycle` seconds. `cycle` must be greater than `0`.
 * `msg_rcv`: | `msg_name: Name, msg_type: ACLPerformative` | Fires upon receiving message matching name `msg_name` and `msg_type`.

`EBEHAV` | - | Exists behaviour scope. Has to correspond to `BEHAV`

*Example usage:*
```aasm
BEHAV read_message, msg_rcv, test_message, inform
#
# behaviour definition here
#
EBEHAV
```

`MESSAGE` | **args:** `name: Name, performative: ACLPerformative` | Enters the scope for describing a Message of specified name and performative

`EMESSAGE` | - | Exists message scope. Has to correspond to `MESSAGE`.

*Example usage:*
```aasm
MESSAGE test_message, inform
#
# message definitnion here
#
EMESSAGE
```

`AGENT` | **args:** `name: Name` | Enters the scope for describing an agent.

`EAGENT` | - | Exists agent scope. Has to correspond to `AGENT`

*Example usage*
```aasm
AGENT
#
# agent definition here
#
EAGENT
```
