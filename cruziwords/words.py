import csv
from typing import Any, Iterable, NamedTuple


class Word(NamedTuple):
    """
    A word that can be placed on a crossword puzzle, consisting of a clue and a solution.
    """

    clue: str
    solution: str

    def __len__(self) -> int:
        """
        :return: Length of the solution.
        """
        return len(self.solution)

    def __getitem__(self, pos: Any) -> Any:
        """
        :param pos: Letter index.
        :return: The n'th letter of the solution.
        """
        return self.solution[pos]


class WordsCorpus:
    """
    A set of words that can be placed on a crossword puzzle. Used during construction of suitable puzzles.

    Designed to be immutable so that it can be used in recursive algorithms.
    """

    def __init__(self, words: Iterable[Word]):
        self.words = set(words)

    def __len__(self) -> int:
        return len(self.words)

    def __iter__(self) -> Iterable[Word]:
        return iter(self.words)

    def pop(self, word: Word) -> "WordsCorpus":
        """
        :param word: Word to remove from this corpus (signifying that it's been successfully placed on a crossword).
        :return: A new `WordsCorpus`, with `word` removed. Raises a `KeyError` if this corpus never contained `word`.
        """
        words = self.words.copy()
        words.remove(word)
        return WordsCorpus(words)

    def containing(self, letter: str) -> Iterable[tuple[Word, int]]:
        """
        :param letter: Which words contain this letter?
        :return: Yields all words which contain a certain letter, including the position the letter has in that word.
        """
        for word in self.words:
            if letter in word.solution:  # This line speeds up the code significantly
                for i, _letter in enumerate(word.solution):
                    if _letter == letter:
                        yield word, i

    @classmethod
    def from_csv_file(cls, csv_path: str) -> "WordsCorpus":
        """
        Construct a word corpus from a CSV file. Clue goes in the first column, and then one or more solutions in the
        following columns. For example:

            Capital of Spain,MADRID
            Historic capital of Spain,TOLEDO,CORDOBA

        :param csv_path: Path to CSV file.
        """

        def words_from_csv() -> Iterable[Word]:
            for row in csv_reader:
                definition = row[0]
                for alt_word in row[1:]:
                    if definition and alt_word:
                        yield Word(row[0], alt_word)

        with open(csv_path, "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            words = words_from_csv()
            return cls(words)
