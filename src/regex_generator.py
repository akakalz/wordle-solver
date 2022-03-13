from typing import Dict
from renderer import Comparison


ALPHA = {
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
}


class Rules:
    def __init__(self, letter_count: int = 5) -> None:
        self.letter_count = letter_count

        self.dead_letters: set = set()
        self.right_indexes: Dict[int, set] = dict()
        self.wrong_indexes: dict = dict()
        self.must_haves: set = set()

    def generate_regex(self) -> str:
        return "".join([
            f"[{''.join(self._generate_index_char_set(x))}]"
            for x in range(self.letter_count)
        ])

    def _generate_index_char_set(self, idx: int) -> set:
        if idx in self.right_indexes:
            return {self.right_indexes[idx]}
        else:
            return self._generate_char_set_for_index(idx)

    def _generate_char_set_for_index(self, idx: int) -> set:
        return ALPHA - self.dead_letters - set(self.wrong_indexes.get(idx, set()))

    def ingest_comparison(self, comparison: Dict[int, Comparison]) -> None:
        for k, v in comparison.items():
            if v.letter_in_correct_location:
                self.right_indexes[k] = v.letter
                self.must_haves.add(v.letter)
            elif v.letter_in_answer:
                if k not in self.wrong_indexes:
                    self.wrong_indexes[k] = set()
                self.wrong_indexes[k].add(v.letter)
                self.must_haves.add(v.letter)
            else:
                self.dead_letters.add(v.letter)
