from .test_puzzle import baghdad, kabul, puzzle  # noqa: F401

from cruziwords.puzzle import Direction, Position, Puzzle
from cruziwords.scoring import calculate_density, count_checked_squares, count_words
from cruziwords.words import Word


def test_count_checked_squares(puzzle: Puzzle, kabul: Word, baghdad: Word):
    puzzle = (
        puzzle
        .add_word(kabul, Position(-2, 0), Direction.ACROSS)
        .add_word(baghdad, Position(0, -2), Direction.DOWN)
    )

    assert count_checked_squares(puzzle) == 1


def test_calculate_density(puzzle: Puzzle, kabul: Word, baghdad: Word):
    assert calculate_density(puzzle) == 0

    puzzle = puzzle.add_word(kabul, Position(-2, 0), Direction.ACROSS)
    assert calculate_density(puzzle) == 1

    puzzle = puzzle.add_word(baghdad, Position(0, -2), Direction.DOWN)
    assert 0 < calculate_density(puzzle) < 1


def test_count_words(puzzle: Puzzle, kabul: Word):
    puzzle = (
        puzzle
        .add_word(kabul, Position(0, 0), Direction.ACROSS)
        .add_word(kabul, Position(2, -2), Direction.DOWN)
    )

    word_count = count_words(puzzle)

    assert word_count == 2
