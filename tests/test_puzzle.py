import pytest

from cruziwords.puzzle import Direction, InvalidOperation, Position, Puzzle, WordEnd
from cruziwords.words import Word


@pytest.fixture
def puzzle() -> Puzzle:
    return Puzzle()


@pytest.fixture
def kabul() -> Word:
    return Word("Capital of Afghanistan", "KABUL")


@pytest.fixture
def baghdad() -> Word:
    return Word("Capital of Iraq", "BAGHDAD")


def test_empty_puzzle():
    puzzle = Puzzle()
    assert puzzle[0, 0] is None


def test_add_word(puzzle: Puzzle, kabul: Word):
    new_puzzle = puzzle.add_word(kabul, Position(0, 0), Direction.ACROSS)

    assert puzzle[0, 0] is None

    assert new_puzzle[0, 0].word == kabul
    assert new_puzzle[0, 0].dir == Direction.ACROSS

    assert new_puzzle[1, 0].letter == "K"
    assert new_puzzle[2, 0].letter == "A"
    assert new_puzzle[3, 0].letter == "B"
    assert new_puzzle[4, 0].letter == "U"
    assert new_puzzle[5, 0].letter == "L"

    assert type(new_puzzle[6, 0]) is WordEnd


def test_puzzle_dimensions(puzzle: Puzzle, kabul: Word):
    assert puzzle.top_left == puzzle.bottom_right == Position(0, 0)

    puzzle = (
        puzzle
        .add_word(kabul, Position(0, 0), Direction.ACROSS)
        .add_word(kabul, Position(2, -2), Direction.DOWN)
    )

    assert puzzle.top_left == Position(0, -2)
    assert puzzle.bottom_right == Position(5, 3)

    assert puzzle.width == 6
    assert puzzle.height == 6


def test_add_word_collision(puzzle: Puzzle, kabul: Word):
    puzzle = puzzle.add_word(kabul, Position(0, 0), Direction.ACROSS)

    with pytest.raises(InvalidOperation):
        puzzle.add_word(kabul, Position(0, 0), Direction.ACROSS)

    with pytest.raises(InvalidOperation):
        puzzle.add_word(kabul, Position(4, 0), Direction.DOWN)

    with pytest.raises(InvalidOperation):
        puzzle.add_word(kabul, Position(4, -1), Direction.DOWN)

    with pytest.raises(InvalidOperation):
        puzzle.add_word(kabul, Position(6, -1), Direction.DOWN)


def test_add_word_intersection(puzzle: Puzzle, kabul: Word, baghdad: Word):
    puzzle = (
        puzzle
        .add_word(kabul, Position(-2, 0), Direction.ACROSS)
        .add_word(baghdad, Position(0, -2), Direction.DOWN)
    )

    assert puzzle[0, 0].letter == "A"
    assert len(puzzle[0, 0].words) == 2
