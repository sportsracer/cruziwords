from typing import Callable, TypeAlias

from .puzzle import Letter, Puzzle, WordEnd, WordStart

ScoreFuncType: TypeAlias = Callable[[Puzzle], int | float]


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


def count_words(puzzle: Puzzle) -> int:
    """
    Method that returns the number of words used in the puzzle.
    :param puzzle: Puzzle to assess
    :return: The count of words
    """
    word_count: int = 0

    for _, cell in puzzle:
        if type(cell) is WordStart:
            word_count += 1

    return word_count


def score_puzzle(puzzle: Puzzle) -> float:
    """
    Scoring function which favors puzzles with more checked squares, using density as a tiebreaker.
    """
    return count_checked_squares(puzzle) + calculate_density(puzzle)
