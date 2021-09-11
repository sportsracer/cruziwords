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
    A square on a crossword puzzle that is the start of a word.
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
    def dimensions(self) -> tuple[int, int, int, int]:
        """
        If board were extended to a rectangle, calculate its dimensions.
        :return: Tuple of (left, top, right, bottom) coordinates.
        """
        visible_positions = [pos for pos, square in self.__positions.items() if type(square) is not WordEnd]

        if not visible_positions:
            return 0, 0, 0, 0

        first_pos = visible_positions[0]
        left = right = first_pos.col
        top = bottom = first_pos.row

        for col, row in visible_positions[1:]:
            if row < top:
                top = row
            elif row > bottom:
                bottom = row

            if col < left:
                left = col
            elif col > right:
                right = col

        return left, top, right, bottom

    @cached_property
    def left(self) -> int:
        return self.dimensions[0]

    @cached_property
    def top(self) -> int:
        return self.dimensions[1]

    @cached_property
    def right(self) -> int:
        return self.dimensions[2]

    @cached_property
    def bottom(self) -> int:
        return self.dimensions[3]

    @cached_property
    def width(self) -> int:
        return self.right - self.left + 1

    @cached_property
    def height(self) -> int:
        return self.bottom - self.top + 1

    def add_word(self, word: Word, start_pos: Position, dir: Direction) -> "Puzzle":
        """
        Add a word and return a new puzzle, if word placement is valid, otherwise raising `InvalidOperation`.
        :param word: Word to place on puzzle.
        :param start_pos: Starting position.
        :param dir: Direction for the word to go; down or right.
        :return: A new puzzle with the new word added.
        """
        # A word can only start on an empty square, or another word's end
        start_square = self.__positions.get(start_pos)
        if not (start_square is None or type(start_square) is WordEnd):
            raise InvalidOperation()

        # Keep track of the changes we'll need to apply to the new copy of this board
        changes: dict[Position, SquareType] = {start_pos: WordStart(word, dir)}

        # A word can only end on an empty square, or another word's start or end
        end_pos = start_pos.move(len(word) + 1, dir)
        end_square = self.__positions.get(end_pos)
        if end_square is None:
            changes[end_pos] = WordEnd()
        elif type(end_square) not in {WordStart, WordEnd}:
            raise InvalidOperation()

        # A letter can only be placed on an empty square, or an identical letter
        for i in range(len(word)):
            pos = start_pos.move(i + 1, dir)
            existing_letter = self.__positions.get(pos)
            if existing_letter is None:
                changes[pos] = Letter(word[i], frozenset([word]))
            elif type(existing_letter) is Letter and existing_letter.letter == word[i]:
                changes[pos] = Letter(word[i], frozenset(existing_letter.words | {word}))
            else:
                raise InvalidOperation()

        # If we got this far, the word placement is valid. Make a copy of this board's positions with the changes, and
        # construct a new instance.
        new_positions = self.__positions | changes
        return Puzzle(new_positions)
