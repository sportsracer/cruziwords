from ..puzzle import Direction, Letter, Puzzle, SquareType, WordStart


def print_square(square: SquareType) -> str:
    """
    Render a cell to the terminal (or any place with unformatted fixed-width font).
    """
    match square:
        case WordStart(dir=dir):
            return f" {'▶' if dir == Direction.ACROSS else '▼'} "
        case Letter(letter=letter):
            return f" {letter} "
        case _:
            return "   "


def print_solution(puzzle: Puzzle) -> None:
    """
    Print the solution of a crossword puzzle to the command line.
    """
    for row in range(puzzle.top, puzzle.bottom + 1):
        printed_row = "".join(print_square(puzzle[col, row]) for col in range(puzzle.left, puzzle.right + 1))
        print(printed_row)
