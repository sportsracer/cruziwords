import csv, re
from pathlib import Path
from typing import Any, Iterable, Iterator, NamedTuple, Union


def normalize(raw_solution: str) -> str:
    """
    Method that normalizes the solutions used in the puzzle taken that the input file does not have a defined final format
    In many languages the accents in vowels are omitted in crosswords puzzles, letters are considered uppercase only etc
    Valid for French, Italian, Spanish, German ...
    source https://en.wikipedia.org/wiki/Crossword#Orthography
    """
    raw_solution_upper = raw_solution.upper()
    raw_solution_upper = re.sub(u"[ÀÁÂÃÅ]", "A", raw_solution_upper)
    raw_solution_upper = re.sub(u"[ÈÉÊ]", "E", raw_solution_upper)
    raw_solution_upper = re.sub(u"[ÌÍÎ]", "I", raw_solution_upper)
    raw_solution_upper = re.sub(u"[ÒÓÔÕ]", "O", raw_solution_upper)
    raw_solution_upper = re.sub(u"[ÙÚÛ]", "U", raw_solution_upper)
    raw_solution_upper = re.sub(u"[ÝŸ]", "Y", raw_solution_upper)
    raw_solution_upper = re.sub("Ä", "AE", raw_solution_upper)  # Replace pattern Ä -> AE as in German
    raw_solution_upper = re.sub("Ü", "UE", raw_solution_upper)  # Replace pattern Ü -> UE as in German
    raw_solution_upper = re.sub("Ö", "OE", raw_solution_upper)  # Replace pattern Ö -> OE as in German
    return raw_solution_upper


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

    def __iter__(self) -> Iterator[Word]:
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
    def from_csv_string(cls, csv_string: str) -> "WordsCorpus":
        """
        Construct a word corpus from an in-memory CSV file.
        :param csv_string: A CSV file read in memory.
        """
        csv_lines = csv_string.splitlines()
        csv_reader = csv.reader(csv_lines)

        def words_from_csv() -> Iterable[Word]:
            for row in csv_reader:
                definition = row[0]
                for alt_word in row[1:]:
                    if definition and alt_word:
                        yield Word(row[0], normalize(alt_word))

        words = words_from_csv()
        return cls(words)

    @classmethod
    def from_csv_file(cls, csv_path: Union[str, Path]) -> "WordsCorpus":
        """
        Construct a word corpus from a CSV file. Clue goes in the first column, and then one or more solutions in the
        following columns. For example:

            Capital of Spain,MADRID
            Historic capital of Spain,TOLEDO,CORDOBA

        :param csv_path: Path to CSV file.
        """
        with open(csv_path, "r", encoding="utf-8") as csv_file:
            csv_string = csv_file.read()
            return cls.from_csv_string(csv_string)
