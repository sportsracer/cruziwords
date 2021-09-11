# Cruziwords

Crosswords puzzle generator. The name *cruziwords* is a mix of the Spanish and English terms for crosswords puzzle.

This script is supposed to be used with just a few dozen input words. It will try to place all of them in a dense
puzzle. Use it, for example, for thematic quizzes, family games …

![European capitals](doc/european-capitals.png)

## Installation

Requires Python 3.9.

```shell
# Install cruziwords in a virtual environment in development mode
python3.9 -m venv venv
. venv/bin/activate
pip install -e .
```

## Usage

```shell
# Create a crossword puzzle, picking a random example
cruziwords

# Specify your own clues and solutions, and render the puzzle to an HTML file
cruziwords CSV_FILE --html-out HTML_FILE
```

For specifying your own words, this is the format. It's possible to supply multiple possible solutions to the same
clue. The program will try to place all of them.

```
Capital of Germany,BERLIN
European capital,MADRID,PARIS
```

## Development

```shell
pip install tox

# Lint
tox -e black

# Check types
tox -e mypy

# Run tests
tox -e py

# … or all at once!
tox
```

Try playing with the [scoring functions](cruziwords/scoring.py) to see how that affects the shape of the selected
puzzle!