from regex_generator import Rules
from renderer import Comparison
import pytest


@pytest.mark.parametrize(
    "comparison,dead_letters,right_indexes,wrong_indexes,must_haves",
    [
        (
            {0: Comparison("a", False, False), 1: Comparison("b", False, False), 2: Comparison("c", False, False), 3: Comparison("d", False, False), 4: Comparison("e", False, False)},
            {"a","b","c","d","e"},
            {},
            {},
            set(),
        ),
        (
            {0: Comparison("a", True, False), 1: Comparison("b", False, False), 2: Comparison("c", False, False), 3: Comparison("d", False, False), 4: Comparison("e", False, False)},
            {"b","c","d","e"},
            {},
            {0: {"a"}},
            {"a"},
        ),
        (
            {0: Comparison("a", True, False), 1: Comparison("b", True, True), 2: Comparison("c", False, False), 3: Comparison("d", False, False), 4: Comparison("e", False, False)},
            {"c","d","e"},
            {1: "b"},
            {0: {"a"}},
            {"a", "b"},
        ),
    ]
)
def test_ingest_comparison(comparison, dead_letters, right_indexes, wrong_indexes, must_haves):
    # arrange
    test_rule = Rules()
    # act
    test_rule.ingest_comparison(comparison)
    # assert
    assert test_rule.dead_letters == dead_letters
    assert test_rule.right_indexes == right_indexes
    assert test_rule.wrong_indexes == wrong_indexes
    assert test_rule.must_haves == must_haves
