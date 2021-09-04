import pytest

from cruziwords.search import search_puzzle
from cruziwords.scoring import score_puzzle
from cruziwords.words import Word, WordsCorpus


@pytest.fixture
def words():
    return WordsCorpus([
        Word("Swedish band", "ABBA"),
        Word("Female first name", "ANNA"),
        Word("Italian car brand", "ALFA"),
        Word("Screaming sound", "AAAA"),
    ])


def test_search(words: WordsCorpus):
    # Test that these words are successfully arranged into a square
    puzzle = search_puzzle(words, score_puzzle)
    assert puzzle.width == 5
    assert puzzle.height == 5
