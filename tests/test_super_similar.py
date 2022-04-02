from research.super_similar_words import SuperSimilar
import pytest


@pytest.mark.parametrize(
    "words,expected",
    [
        (set(), False),
        ({"match", "batch", "hatch", "catch"}, True),
        ({"words", "sword"}, False),
        ({"rando", "mando", "cando", "wrong"}, True),
        ({"abcde", "bcdef", "cdefg", "defgh", "efghi", "fghij"}, False)
    ]
)
def test_has_super_similar(words, expected):
    # arrange
    obj = SuperSimilar(words)
    # act
    actual = obj.has_super_similar()
    # assert
    assert actual == expected
