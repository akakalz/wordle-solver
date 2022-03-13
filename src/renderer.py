from dataclasses import dataclass
from constants import Constants
from typing import List


BLACK = ":black_large_square:"
WHITE = ":white_large_square:"
GREEN = ":large_green_square:"
YELLOW = ":large_yellow_square:"


@dataclass
class Comparison:
    letter: str
    letter_in_answer: bool
    letter_in_correct_location: bool


class WordCompare:
    def __init__(self, word: str, answer: str) -> None:
        self._word: str = word
        self._answer: str = answer
        self.comparison: dict = dict()

        self._compare()

    def _compare(self) -> None:
        for idx, letter in enumerate(self._word):
            self.comparison[idx] = Comparison(
                letter=letter,
                letter_in_answer=(True if letter in self._answer else False),
                letter_in_correct_location=(True if self._answer[idx] == letter else False),
            )


class Renderer:
    def __init__(self, constants: Constants, comparisons: List[dict], dark_mode: bool = True) -> None:
        self.constants = constants
        self.comparisons: List[dict] = comparisons
        self.dark_mode = dark_mode
        # self._answer = self.constants.answers.get(str(self.constants.today))

    def render(self) -> str:
        """
        Wordle 266 3/6

        🟩🟩🟨🟨🟩
        ⬛🟩⬛⬛🟨
        🟩🟩🟩🟩🟩
        """
        return "\n".join(
            [self._generate_header()] + [self._render_comparison(x) for x in self.comparisons]
        )

    def _render_comparison(self, comparison: dict) -> str:
        blocks = []
        for _, v in comparison.items():
            if v.letter_in_correct_location:
                block = GREEN
            elif v.letter_in_answer:
                block = YELLOW
            elif self.dark_mode:
                block = BLACK
            else:
                block = WHITE
            blocks.append(block)
        return "".join(blocks)

    def _generate_header(self) -> str:
        number = (self.constants.today - self.constants.start_date).days
        for i, cmp in enumerate(self.comparisons):
            if all([v.letter_in_correct_location for _, v in cmp.items()]):
                guesses_till_correct = str(i + 1)
                break
        else:
            guesses_till_correct = "X"
        return f"Wordle {number} {guesses_till_correct}/6\n"
