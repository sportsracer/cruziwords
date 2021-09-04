from enum import Enum
from functools import cached_property
from typing import Iterator, NamedTuple, Optional, Union

from .words import Word


class Direction(Enum):
    """
    Direction in which one can move on a crossword puzzle.
    """

    ACROSS = 1
    DOWN = 2


class Position(NamedTuple):
    """
    Position on a crossword puzzle, identified by its column and row. Both can be negative!
    """

    col: int
    row: int

    def move(self, step: int, direction: Direction) -> "Position":
        if direction == Direction.ACROSS:
            return Position(self.col + step, self.row)

        if direction == Direction.DOWN:
            return Position(self.col, self.row + step)

        raise ValueError()


class WordStart(NamedTuple):
    """
    A sqzare on a crossword puzzle that is the start of a word.
    """

    word: Word
    dir: Direction


class Letter(NamedTuple):
    """
    A square on a crossword puzzle that is a letter belong to one or two words.
    """

    letter: str
    words: frozenset[Word]


class WordEnd:
    """
    A square on a crossword puzzle that immediately follows the last letter of a word. Such squares are usually not
    visualized, but are useful to avoid certain invalid puzzle states.
    """


SquareType = Union[WordStart, Letter, WordEnd]


class InvalidOperation(Exception):
    """
    Custom exception that is thrown when attempting to modify a puzzle would result in an invalid state.
    """


class Puzzle:
    """
    A crossword puzzle, modeled as a mapping of (column, row) positions to squares.

    This class is designed to be immutable; the only way to modify it is by calling `add_word`, which returns a new
    puzzle.
    """

    def __init__(self, positions: Optional[dict[Position, SquareType]] = None):
        """
        :param positions: Mapping of positions to squares. Not expected to be set by caller; use `add_word` to construct
        puzzles instead.
        """
        self.__positions = positions or {}

    def __getitem__(self, col_row: tuple[int, int]) -> Optional[SquareType]:
        """
        For accessing a square like this: `puzzle[2, 3]`.
        :param col_row: Column and row indices.
        :return: The square which is at this position, or `None`.
        """
        pos = Position(*col_row)
        return self.__positions.get(pos)

    def __iter__(self) -> Iterator[tuple[Position, SquareType]]:
        """
        Yield (position, square) pairs.
        """
        return iter(self.__positions.items())

    @cached_property
    def top_left(self) -> Position:
        """
        :return: The position of the top left corner, if this puzzle were extended to be a rectangle.
        """
        if len(self.__positions) == 0:
            return Position(0, 0)
        return Position(
            min(pos.col for pos in self.__positions),
            min(pos.row for pos in self.__positions),
        )

    @cached_property
    def bottom_right(self) -> Position:
        """
        :return: The position of the bottom right corner, if this puzzle were extended to be a rectangle.
        """
        if len(self.__positions) == 0:
            return Position(0, 0)
        return Position(
            max(pos.col for pos, square in self.__positions.items() if type(square) is not WordEnd),
            max(pos.row for pos, square in self.__positions.items() if type(square) is not WordEnd),
        )

    @cached_property
    def width(self) -> int:
        """
        :return: Maximum horizontal extension of this puzzle.
        """
        return self.bottom_right.col - self.top_left.col

    @cached_property
    def height(self) -> int:
        """
        :return: Maximum vertical extension of this puzzle.
        """
        return self.bottom_right.row - self.top_left.row

    def add_word(self, word: Word, start_pos: Position, dir: Direction) -> "Puzzle":
        """
        Add a word and return a new puzzle, if word placement is valid, otherwise raising `InvalidOperation`.
        :param word: Word to place on puzzle.
        :param start_pos: Starting position.
        :param dir: Direction for the word to go; down or right.
        :return: A new puzzle with the new word added.
        """
        # A word can only start on an empty square, or another word's end
        if not (start_pos not in self.__positions or type(self.__positions[start_pos]) is WordEnd):
            raise InvalidOperation()

        # Keep track of the changes we'll need to apply to the new copy of this board
        changes: dict[Position, SquareType] = {start_pos: WordStart(word, dir)}

        # A word can only end on an empty square, or another word's start or end
        end_pos = start_pos.move(len(word) + 1, dir)
        if end_pos not in self.__positions:
            changes[end_pos] = WordEnd()
        elif type(self.__positions[end_pos]) not in {WordStart, WordEnd}:
            raise InvalidOperation()

        # A letter can only be placed on an empty square, or an identical letter
        for i in range(len(word)):
            pos = start_pos.move(i + 1, dir)
            existing_letter: Letter
            if pos not in self.__positions:
                changes[pos] = Letter(word[i], frozenset([word]))
            elif type(existing_letter := self.__positions[pos]) is Letter and existing_letter.letter == word[i]:  # type: ignore
                changes[pos] = Letter(word[i], frozenset(existing_letter.words | {word}))
            else:
                raise InvalidOperation()

        # If we got this far, the word placement is valid. Make a copy of this board's positions, and construct a new
        # instance.
        new_positions = self.__positions.copy() | changes
        return Puzzle(new_positions)
