from functools import singledispatch
from typing import Optional

from ..puzzle import Direction, Letter, Puzzle, WordEnd, WordStart


@singledispatch
def print_cell(cell: Optional[WordEnd]) -> str:
    """
    Return CLI representation of a single cell.
    """
    return "   "


@print_cell.register
def _(cell: WordStart) -> str:
    return f" {'▶' if cell.dir == Direction.ACROSS else '▼'} "


@print_cell.register
def __(cell: Letter) -> str:
    return f" {cell.letter} "


def print_solution(puzzle: Puzzle) -> None:
    """
    Print the solution of a crossword puzzle to the command line.
    """
    for row in range(puzzle.top, puzzle.bottom + 1):
        printed_row = "".join(print_cell(puzzle[col, row]) for col in range(puzzle.left, puzzle.right + 1))
        print(printed_row)
