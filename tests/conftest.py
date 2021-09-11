import pytest

from cruziwords.words import Word


@pytest.fixture
def kabul() -> Word:
    return Word("Capital of Afghanistan", "KABUL")


@pytest.fixture
def baghdad() -> Word:
    return Word("Capital of Iraq", "BAGHDAD")
