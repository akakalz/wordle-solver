from rules_generator import Rules
from renderer import Comparison
import pytest


@pytest.mark.parametrize(
    "comparison,dead_letters,right_indexes,wrong_indexes,must_haves",
    [
        (
            {0: Comparison("a", False, False, False, 0), 1: Comparison("b", False, False, False, 0), 2: Comparison("c", False, False, False, 0), 3: Comparison("d", False, False, False, 0), 4: Comparison("e", False, False, False, 0)},
            {"a","b","c","d","e"},
            {},
            {},
            set(),
        ),
        (
            {0: Comparison("a", True, False, False, 1), 1: Comparison("b", False, False, False, 0), 2: Comparison("c", False, False, False, 0), 3: Comparison("d", False, False, False, 0), 4: Comparison("e", False, False, False, 0)},
            {"b","c","d","e"},
            {},
            {0: {"a"}},
            {"a"},
        ),
        (
            {0: Comparison("a", True, False, False, 1), 1: Comparison("b", True, True, False, 1), 2: Comparison("c", False, False, False, 0), 3: Comparison("d", False, False, False, 0), 4: Comparison("e", False, False, False, 0)},
            {"c","d","e"},
            {1: "b"},
            {0: {"a"}},
            {"a", "b"},
        ),
    ]
)
def test_ingest_comparisons(comparison, dead_letters, right_indexes, wrong_indexes, must_haves):
    # arrange
    test_rule = Rules()
    # act
    test_rule.ingest_comparisons(comparison)
    # assert
    assert test_rule.dead_letters == dead_letters
    assert test_rule.right_indexes == right_indexes
    assert test_rule.wrong_indexes == wrong_indexes
    assert test_rule.must_haves == must_haves
