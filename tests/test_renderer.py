from renderer import (
    BLACK,
    Comparison,
    Renderer,
    WordCompare,
    GREEN,
)
from constants import Constants
import pytest


@pytest.mark.parametrize(
    "letter,in_answer,in_loc",
    [
        ("a", True, True),
        ("a", False, True),
        ("a", True, False),
        ("a", False, False),
    ]
)
def test_comparison(letter, in_answer, in_loc):
    # arrange
    # act
    actual = Comparison(letter=letter, letter_in_answer=in_answer, letter_in_correct_location=in_loc)
    # assert
    assert actual.letter == letter
    assert actual.letter_in_answer == in_answer
    assert actual.letter_in_correct_location == in_loc


@pytest.mark.parametrize(
    "word,answer,expected",
    [
        ("toner","today", {0: Comparison("t", True, True), 1: Comparison("o", True, True),
                            2: Comparison("n", False, False), 3: Comparison("e", False, False),
                            4: Comparison("r", False, False)}),
        ("today","today", {0: Comparison("t", True, True), 1: Comparison("o", True, True),
                            2: Comparison("d", True, True), 3: Comparison("a", True, True),
                            4: Comparison("y", True, True)}),
        ("sonar","today", {0: Comparison("s", False, False), 1: Comparison("o", True, True),
                            2: Comparison("n", False, False), 3: Comparison("a", True, True),
                            4: Comparison("r", False, False)}),
    ]
)
def test_word_compare(word, answer, expected):
    # arrange
    # act
    test_obj = WordCompare(word, answer)
    # assert
    assert test_obj.comparison == expected


@pytest.mark.parametrize(
    "answer,guesses,expected",
    [
        ("clear", ["clear"], f"Wordle 0 1/6\n\n{GREEN}{GREEN}{GREEN}{GREEN}{GREEN}"),
        ("cigar", ["clear", "cigar"], f"Wordle 0 2/6\n\n{GREEN}{BLACK}{BLACK}{GREEN}{GREEN}\n{GREEN}{GREEN}{GREEN}{GREEN}{GREEN}"),
        ("cigar", ["zzzzz", "zzzzz", "zzzzz", "zzzzz", "zzzzz", "zzzzz"], f"Wordle 0 X/6\n\n{BLACK}{BLACK}{BLACK}{BLACK}{BLACK}\n{BLACK}{BLACK}{BLACK}{BLACK}{BLACK}\n{BLACK}{BLACK}{BLACK}{BLACK}{BLACK}\n{BLACK}{BLACK}{BLACK}{BLACK}{BLACK}\n{BLACK}{BLACK}{BLACK}{BLACK}{BLACK}\n{BLACK}{BLACK}{BLACK}{BLACK}{BLACK}"),
    ]
)
def test_renderer(answer, guesses, expected):
    # arrange
    const = Constants()
    const.today = const.start_date  # just assume it's day 1 for brevity
    compares = [WordCompare(guess, answer).comparison for guess in guesses]
    test_obj = Renderer(const, compares)
    # act
    actual = test_obj.render()
    # assert
    assert actual == expected
