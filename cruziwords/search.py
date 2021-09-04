import logging
import random
from itertools import groupby
from operator import itemgetter
from typing import Iterable, Optional

from .puzzle import Direction, InvalidOperation, Letter, Position, Puzzle
from .scoring import ScoreFuncType
from .search_frontier import SearchFrontier
from .words import Word, WordsCorpus

LOGGER = logging.getLogger(__file__)


def greedy_search(words: WordsCorpus, puzzle: Puzzle, score_func: ScoreFuncType, depth: int = 0) -> Iterable[Puzzle]:
    """
    Try different placements of words on puzzle recursively. At each iteration, keep exploring a small number of the
    most desirable intermediate puzzles (hence the greedy).

    :param words: Words that should still be placed.
    :param puzzle: Intermediate state of the puzzle we're exploring.
    :param score_func: Callable to assign a desirability score to puzzle.
    :param depth: Recursion depth; used to control the breadth of our search.
    :return: Yields puzzles which are discovered by this search.
    """
    # As we progress deeper, limit the search frontier so that we converge at some point
    frontier = SearchFrontier(score_func, max(3 - depth, 1))

    # Sort and group same letters to speed up the search
    letters_sorted = sorted(
        ((pos_cell[0], pos_cell[1].letter) for pos_cell in puzzle if type(pos_cell[1]) is Letter),
        key=itemgetter(1),
    )
    letters_grouped = groupby(letters_sorted, key=itemgetter(1))

    letter: str
    for letter, positions_group in letters_grouped:

        # Convert to list so we can iterate multiple times
        positions = list(pos for pos, _ in positions_group)
        random.shuffle(positions)

        for possible_word, i in words.containing(letter):
            for pos in positions:
                for dir in Direction:
                    start_pos = pos.move(-i - 1, dir)
                    try:
                        new_puzzle = puzzle.add_word(possible_word, start_pos, dir)
                    except InvalidOperation:
                        continue
                    else:
                        new_words = words.pop(possible_word)
                        frontier.consider(new_puzzle, new_words)

    if not frontier.empty:
        # We've found possible word placements - keep exploring recursively
        for best_puzzle, best_words in frontier:
            yield from greedy_search(best_words, best_puzzle, score_func, depth + 1)
    else:
        # No further words could be placed - we've reached the base case
        yield puzzle


def search_puzzle(words: WordsCorpus, score_func: ScoreFuncType, max_iterations: Optional[int] = None) -> Puzzle:
    """
    Create a nice puzzle which contains as many words from words corpus as can be placed.
    :param words: Words that should be placed.
    :param score_func: Callable to assign a desirability score to puzzle.
    :param max_iterations: Stop finding a more desirable puzzle after this many iterations.
    :return: The best puzzle discovered by this search.
    """
    # Place the longest word first.
    first_word = max(words, key=Word.__len__)  # type: ignore
    words = words.pop(first_word)
    start_puzzle = Puzzle().add_word(first_word, Position(0, 0), Direction.DOWN)

    iterations = 0
    best_puzzle = start_puzzle
    best_score = None

    try:
        for next_puzzle in greedy_search(words, start_puzzle, score_func):
            next_score = score_func(next_puzzle)
            if best_score is None or next_score > best_score:
                best_score = next_score
                best_puzzle = next_puzzle

                LOGGER.debug(
                    "Best score updated to %.4f after %d iterations",
                    next_score,
                    iterations,
                )

            iterations += 1
            if max_iterations is not None and iterations >= max_iterations:
                break
    except KeyboardInterrupt:
        LOGGER.warning("Aborting search")

    return best_puzzle
