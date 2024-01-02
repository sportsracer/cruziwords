import heapq
from typing import Any, Iterator, NamedTuple, override

from .puzzle import Puzzle
from .scoring import ScoreFuncType
from .words import WordsCorpus


class SearchFrontier:
    """
    A frontier of crossword puzzles to consider during a search.
    """

    # Helper class for storing score puzzles on a heap.
    class FrontierItem(NamedTuple):
        score: float
        puzzle: Puzzle
        words: WordsCorpus

        @override
        def __lt__(self, other: Any) -> Any:
            return self.score < other.score

        @override
        def __le__(self, other: Any) -> Any:
            return self.score <= other.score

    def __init__(self, score_func: ScoreFuncType, max_items: int):
        """
        :param score_func: Scoring function to judge the desirability of a puzzle.
        :param max_items: Keep the `max_items` most desirable puzzles.
        """
        self.score_func = score_func
        self.max_items = max_items
        self.frontier_items: list[SearchFrontier.FrontierItem] = []

    def consider(self, puzzle: Puzzle, words: WordsCorpus) -> None:
        """
        Consider a new puzzle for the frontier, but only if it's within the `max_items` most desirable crosswords.
        :param puzzle: Puzzle to consider.
        :param words: Remaining words that have yet to be placed on the puzzle; needed for further iterations.
        """
        score = self.score_func(puzzle)
        heap_item = self.FrontierItem(score, puzzle, words)
        if len(self.frontier_items) < self.max_items:
            heapq.heappush(self.frontier_items, heap_item)
        else:
            heapq.heappushpop(self.frontier_items, heap_item)

    def __iter__(self) -> Iterator[tuple[Puzzle, WordsCorpus]]:
        """
        Yield the most desirable (puzzle, words corpus) pairs, in arbitrary order.
        """
        for frontier_item in self.frontier_items:
            yield frontier_item.puzzle, frontier_item.words

    @property
    def empty(self) -> bool:
        return len(self.frontier_items) == 0
