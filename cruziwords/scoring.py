from typing import Callable, Union

from .puzzle import Letter, Puzzle, WordEnd

ScoreFuncType = Callable[[Puzzle], Union[int, float]]


def count_checked_squares(puzzle: Puzzle) -> int:
    """
    :return: How many squares are "checked", i.e. belong to two words crossing at this position?
    """
    return sum(1 for _, cell in puzzle if type(cell) is Letter and len(cell.words) == 2)


def calculate_density(puzzle: Puzzle) -> float:
    """
    :return: If you extend this puzzle to a rectangle, what percentage of squares contains word starts or letters?
    """
    area = puzzle.width * puzzle.height
    if not area:
        return 0
    filled_cells = sum(1 for _, cell in puzzle if type(cell) is not WordEnd)
    return filled_cells / area


def score_puzzle(puzzle: Puzzle) -> float:
    """
    Scoring function which favors puzzles with more checked squares, using density as a tiebreaker.
    """
    return count_checked_squares(puzzle) + calculate_density(puzzle)
