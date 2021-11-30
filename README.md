# AA Translator

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Structure](#structure)

## About <a name = "about"></a>

A translator from Agents Assembly to SPADE (Python).

## Getting Started <a name = "getting_started"></a>

### Prerequisites

```
pipenv
```

### Installing

```
pipenv install
```

## Usage <a name = "usage"></a>

Translate agent.aa to SPADE:
```
python translate.py agent.aa
```

For more information about usage run:
```
python translate.py --help
```

## Structure <a name = "structure"></a>

* `generating`
    * `spade.py` - SPADE code generation from the intermediate representation
* `intermediate`
    * `action.py` - action representation
    * `agent.py` - agent representation
    * `behaviour.py` - behaviour representation
    * `environment.py` - environment representation
    * `message.py` - message representation
    * `param.py` - parameters representation
* `parsing`
    * `environments.py` - parsing environments from `*.aa` files
    * `op.py` - Agents Assembly operations
    * `state.py` - state definition used for the parsing process
* `utils`
    * `validation.py` - variables validation
* `translate.py` - entrypoint
