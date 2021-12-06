# AA Translator

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Structure](#structure)
- [Design](#Design)

## About <a name = "about"></a>

A translator from Agents Assembly to SPADE (Python).

## Getting Started <a name = "getting_started"></a>

### Prerequisites

```
Python 3.10
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
    * `action.py` - actions representation
    * `agent.py` - agents representation
    * `argument.py` - action instructions argument representation
    * `behaviour.py` - behaviours representation
    * `message.py` - messages representation
    * `param.py` - agent/message parameters representation
* `parsing`
    * `parse.py` - parsing environments from Agents Assembly files
    * `op.py` - Agents Assembly operations
    * `state.py` - state definition used for the parsing process
* `utils`
    * `validation.py` - variables validation
* `translate.py` - entrypoint

## Design <a name = "design"></a>
* `Message`
    * `Parameter`
        * `Type`
* `Agent`
    * `Parameter`
        * `Type`
        * `Value`
    * `Behaviour`
        * `Type`
        * `Parameter`
        * `Received message`
        * `Actions`
            * `Message to be sent`
            * `Block`
                * `Declaration`
                    * `Name`
                    * `Argument`
                        * `Types`
                * `Instruction`
                    * `Argument`
                        * `Types`
                * `Block`
