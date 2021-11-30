# Project Title

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

* `agent.py` - intermediate agent representation
* `environment.py` - intermediate environment representation
* `message.py` - intermediate message representation
* `op.py` - Agents Assembly operations
* `param.py` - intermediate parameters representation
* `parse.py` - parsing environments from `*.aa` files
* `spade_generator.py` - generating SPADE code from the intermediate representation
* `state.py` - state definition used for the parsing process
* `translate.py` - entrypoint
* `utils.py` - set of helper functions
