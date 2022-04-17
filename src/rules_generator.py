from calendar import c
from typing import Dict
from renderer import Evaluation, WordleComparison
from constants import ALPHA


class Rules:
    def __init__(self, word_size: int = 5) -> None:
        self.word_size = word_size

        self.dead_letters: set = set()
        self.right_indexes: Dict[int, set] = dict()
        self.wrong_indexes: Dict[int, set] = dict()
        self.must_haves: set = set()
        self.preferred_letters: set = set()
        self.letter_counts: dict = dict()

    def __repr__(self) -> str:
        return f"""Rules(
    dead_letters={self.dead_letters},
    right_indexes={self.right_indexes},
    wrong_indexes={self.wrong_indexes},
    must_haves={self.must_haves},
    preferred_letters={self.preferred_letters},
    letter_counts={self.letter_counts},
)
"""

    def generate_regex(self) -> str:
        if self.preferred_letters:
            return "".join([
                f"[{''.join(self.preferred_letters)}]"
                for _ in range(self.word_size)
            ])
        return "".join([
            f"[{''.join(self._generate_index_char_set(x))}]"
            for x in range(self.word_size)
        ])

    def _generate_index_char_set(self, idx: int) -> set:
        if idx in self.right_indexes:
            return {self.right_indexes[idx]}
        else:
            return self._generate_char_set_for_index(idx)

    def _generate_char_set_for_index(self, idx: int) -> set:
        return ALPHA - self.dead_letters - set(self.wrong_indexes.get(idx, set()))

    def _update_letter_counts(self, comparisons: Dict[int, WordleComparison]) -> None:
        new_dict = {}
        for v in comparisons.values():
            if v.evaluation in {Evaluation.correct, Evaluation.present}:
                if v.letter not in new_dict:
                    new_dict[v.letter] = 0
                new_dict[v.letter] += 1
                self.letter_counts[v.letter] = max(new_dict[v.letter], self.letter_counts.get(v.letter, 0))

    def _update_indexes(self, comparisons: Dict[int, WordleComparison]) -> None:
        for idx, cmp in comparisons.items():
            if cmp.evaluation == Evaluation.correct:
                self.right_indexes[idx] = cmp.letter
                self.must_haves.add(cmp.letter)
            elif cmp.evaluation == Evaluation.present:
                if idx not in self.wrong_indexes:
                    self.wrong_indexes[idx] = set()
                self.wrong_indexes[idx].add(cmp.letter)
                self.must_haves.add(cmp.letter)
            elif cmp.evaluation == Evaluation.absent and (cmp.letter in self.must_haves or cmp.letter in self.letter_counts):
                if idx not in self.wrong_indexes:
                    self.wrong_indexes[idx] = set()
                self.wrong_indexes[idx].add(cmp.letter)
            else:
                self.dead_letters.add(cmp.letter)

    def ingest_comparisons(self, comparisons: Dict[int, WordleComparison]) -> None:
        self._update_letter_counts(comparisons)
        self._update_indexes(comparisons)
