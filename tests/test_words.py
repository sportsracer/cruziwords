from pathlib import Path

import pytest

from cruziwords.words import Word, WordsCorpus


@pytest.fixture
def words_csv(tmp_path) -> Path:
    csv_content = """Capital of Afghanistan,KABUL
European Capital,BERLIN,MADRID"""
    csv_file = tmp_path / "words.csv"
    csv_file.write_text(csv_content)
    return csv_file


def test_words(words_csv: Path):
    words = WordsCorpus.from_csv_file(str(words_csv))

    assert len(words) == 3
    assert len(set(words)) == 3

    assert any(word.solution == "BERLIN" for word in words)
    assert any(word.solution == "MADRID" for word in words)


def test_pop_word():
    word = Word("Batman's nemesis", "JOKER")
    words = WordsCorpus([word])

    assert len(words) == 1

    new_words = words.pop(word)

    assert len(words) == 1
    assert len(new_words) == 0


def test_words_containing_letter(words_csv: Path):
    words = WordsCorpus.from_csv_file(words_csv)

    assert {(word.solution, i) for word, i in words.containing("I")} == {("BERLIN", 4), ("MADRID", 4)}
    assert not set(words.containing("X"))
