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
    "letter,in_answer,in_loc,many,count_in",
    [
        ("a", True, True, False, 1),
        ("a", False, True, False, 0),
        ("a", True, False, False, 1),
        ("a", False, False, False, 0),
    ]
)
def test_comparison(letter, in_answer, in_loc, many, count_in):
    # arrange
    # act
    actual = Comparison(
        letter=letter,
        letter_in_answer=in_answer,
        letter_in_correct_location=in_loc,
        one_of_many=many,
        count_in_answer=count_in,
    )
    # assert
    assert actual.letter == letter
    assert actual.letter_in_answer == in_answer
    assert actual.letter_in_correct_location == in_loc
    assert actual.one_of_many == many
    assert actual.count_in_answer == count_in


@pytest.mark.parametrize(
    "word,answer,expected",
    [
        ("toner","today", {0: Comparison("t", True, True, False, 1), 1: Comparison("o", True, True, False, 1),
                            2: Comparison("n", False, False, False, 0), 3: Comparison("e", False, False, False, 0),
                            4: Comparison("r", False, False, False, 0)}),
        ("today","today", {0: Comparison("t", True, True, False, 1), 1: Comparison("o", True, True, False, 1),
                            2: Comparison("d", True, True, False, 1), 3: Comparison("a", True, True, False, 1),
                            4: Comparison("y", True, True, False, 1)}),
        ("sonar","today", {0: Comparison("s", False, False, False, 0), 1: Comparison("o", True, True, False, 1),
                            2: Comparison("n", False, False, False, 0), 3: Comparison("a", True, True, False, 1),
                            4: Comparison("r", False, False, False, 0)}),
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
