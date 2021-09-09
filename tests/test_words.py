from pathlib import Path

import pytest

from cruziwords.words import Word, WordsCorpus, normalize


@pytest.fixture
def words_csv(tmp_path) -> Path:
    csv_content = """Capital of Afghanistan,KABUL
European Capital,BERLIN,MADRID
Spain in Spanish,españa
To be in French,ÊTRE
Lice in German,Läuse"""
    csv_file = tmp_path / "words.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    return csv_file


def test_words(words_csv: Path):
    words = WordsCorpus.from_csv_file(str(words_csv))

    assert len(words) == 6
    assert len(set(words)) == 6

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


def test_normalization():
    accented_string = "àéêhelloñçëïßäöü"

    assert normalize(accented_string) == "AEEHELLOÑÇËÏSSAEOEUE"

def test_corpus_normalization(words_csv: Path):
    words = WordsCorpus.from_csv_file(words_csv)

    assert any(word.solution == "ESPAÑA" for word in words)
    assert any(word.solution == "ETRE" for word in words)
    assert any(word.solution == "LAEUSE" for word in words)