from cruziwords.puzzle import Direction, Position, Puzzle
from cruziwords.search_frontier import SearchFrontier
from cruziwords.words import Word, WordsCorpus

from .test_puzzle import kabul, puzzle  # noqa: F401


def test_search_frontier(puzzle: Puzzle, kabul: Word):
    puzzle_with_1_word = puzzle.add_word(kabul, Position(0, 0), Direction.ACROSS)
    puzzle_with_2_words = puzzle_with_1_word.add_word(kabul, Position(0, 1), Direction.ACROSS)

    def number_of_cells(p: Puzzle) -> int:
        return len(list(p))

    frontier = SearchFrontier(number_of_cells, max_items=2)

    words = WordsCorpus([])
    frontier.consider(puzzle, words)
    frontier.consider(puzzle_with_1_word, words)
    frontier.consider(puzzle_with_2_words, words)

    assert set(frontier) == {(puzzle_with_1_word, words), (puzzle_with_2_words, words)}
