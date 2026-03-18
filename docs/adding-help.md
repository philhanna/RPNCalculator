# Adding Help Topics

The built-in help system is implemented in [evaluator/ev_help.py](../evaluator/ev_help.py) as a single class with a `helptext` dict. Users access it with `help <topic>`, `h <topic>`, or `? <topic>`.

## How it works

`EVHelp` is instantiated with a topic string (uppercased by the caller). The constructor looks up the topic in `helptext`, printing the entry if found or an error if not.

## Adding a help entry

Add a key-value pair to `EVHelp.helptext`. The key is the topic name in lowercase; the value is a multi-line string. Keep the format consistent with existing entries:

```python
"square": """
square:  Pops x from the stack and pushes x².
""",
```

For operator symbols, use the symbol itself as the key:

```python
"**": """
**:  Pops x and y from the stack and pushes y ** x (y to the power of x).
""",
```

## Registering the topic in the topic list

The `topics` entry in `helptext` is the index shown when a user types `help topics`. Add your new topic to the appropriate category line:

```python
"topics": """
Arithmetic operations:   +, -, *, /, %, /mod, **, 1+, 1-, abs, int, fact, sqrt, square
...
""",
```

## Conventions

- Topic keys are lowercase even though the lookup is case-insensitive (the caller uppercases the input before passing it, so match the casing used in existing entries — all lowercase).
- <!-- TODO: clarify the actual lookup — does EVHelp lowercase the key before lookup? -->
- The text should describe stack effect using Forth-style notation where appropriate, e.g. `( x -- x² )`.
- Include an example if the usage is non-obvious.

## Testing help

`tests/test_help.py` covers the help system. Add a parametrized case for any new topic:

```python
@pytest.mark.parametrize("topic", ["square"])
def test_help_topic_exists(ev, topic, capsys):
    ev.ev(f"help {topic}")
    captured = capsys.readouterr()
    assert topic in captured.out.lower()
```
