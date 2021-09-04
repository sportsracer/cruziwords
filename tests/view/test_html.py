from cruziwords.view.html import color
from cruziwords.words import Word


def test_color():
    word1 = Word("Kansas state capital", "Topeka")
    word2 = Word("Nebraska state capital", "Lincoln")

    assert color(word1) != color(word2) != color(word1, word2)
