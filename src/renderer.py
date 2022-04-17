from dataclasses import dataclass
from collections import Counter
from re import X
from constants import Constants
from typing import Dict, List
from datetime import date


BLACK = ":black_large_square:"
WHITE = ":white_large_square:"
GREEN = ":large_green_square:"
YELLOW = ":large_yellow_square:"


class Evaluation:
    correct = "correct"
    present = "present"
    absent = "absent"


@dataclass
class Comparison:
    letter: str
    letter_in_answer: bool
    letter_in_correct_location: bool
    one_of_many: bool
    count_in_answer: int


@dataclass
class WordleComparison:
    letter: str
    evaluation: Evaluation


class WordCompare:
    def __init__(self, word: str, answer: str) -> None:
        self._word: str = word
        self._answer: str = answer
        self.comparison: dict = dict()
        self.word_counter = Counter(word)
        self.answer_counter = Counter(answer)

        self._compare()

    def _compare(self) -> None:
        for idx, letter in enumerate(self._word):
            self.comparison[idx] = Comparison(
                letter=letter,
                letter_in_answer=(True if letter in self._answer else False),
                letter_in_correct_location=(True if self._answer[idx] == letter else False),
                one_of_many=self.word_counter[letter] > 1,
                count_in_answer=self.answer_counter[letter],
            )


class WordleCompare:
    def __init__(self, word: str, answer: str) -> None:
        self.word = word
        self.answer = answer

        self.word_counter = Counter(self.word)
        self.answer_counter = Counter(self.answer)

        self._init_evals = self.initial_compare()

        self.second_pass()

    @property
    def comparison(self) -> dict:
        return {
            x[1]: WordleComparison(x[0], x[2])
            for x in self._init_evals
        }

    def __repr__(self) -> str:
        internal = " ".join([
            f"{x[0]}={x[2]}"
            for x in self._init_evals
        ])
        return f"WordleCompare({internal})"

    def initial_compare(self) -> list:
        if len(self.word) != len(self.answer):
            raise ValueError("words are not the same length")
        evaluations = []
        for idx, char in enumerate(self.word):
            if char == self.answer[idx]:
                evaluations.append((char, idx, Evaluation.correct))
            elif char in self.answer:
                evaluations.append((char, idx, Evaluation.present))
            else:
                evaluations.append((char, idx, Evaluation.absent))
        return evaluations

    def second_pass(self) -> None:
        for char, count in self.word_counter.items():
            if char in self.answer and count > self.answer_counter.get(char):
                self.correct_eval(char)

    def correct_eval(self, char: str) -> None:
        indices = [i for i, c in enumerate(self.word) if c == char]
        word_count = self.word_counter.get(char)
        answer_count = self.answer_counter.get(char)
        corrections = word_count - answer_count
        corrected = 0
        while corrected < corrections:
            for idx in indices[::-1]:
                if self._init_evals[idx][2] == Evaluation.present:
                    self._init_evals[idx] = (
                        self._init_evals[idx][0],
                        self._init_evals[idx][1],
                        Evaluation.absent,
                    )
                    corrected += 1
                    break


class Renderer:
    def __init__(
        self,
        constants: Constants,
        comparisons: List[Dict[str, Comparison]],
        dark_mode: bool = True,
    ) -> None:

        self.constants = constants
        self.comparisons = comparisons
        self.dark_mode = dark_mode

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

    def _render_comparison(self, comparison: Dict[str, Comparison]) -> str:
        blocks = []
        for _, v in comparison.items():
            if v.letter_in_correct_location:
                block = GREEN
            elif v.letter_in_answer and not v.one_of_many:
                block = YELLOW
            elif v.letter_in_answer and v.one_of_many and v.count_in_answer:
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


class WordleRenderer:
    def __init__(
        self,
        constants: Constants,
        comparisons: List[Dict[str, Evaluation]],
        dark_mode: bool = True,
    ) -> None:

        self.constants = constants
        self.comparisons = comparisons
        self.dark_mode = dark_mode

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

    def _render_comparison(self, comparison: Dict[str, WordleComparison]) -> str:
        blocks = []
        for _, cmp in comparison.items():
            if cmp.evaluation == Evaluation.correct:
                block = GREEN
            elif cmp.evaluation == Evaluation.present:
                block = YELLOW
            elif self.dark_mode:
                block = BLACK
            else:
                block = WHITE
            blocks.append(block)
        return "".join(blocks)

    def _generate_header(self) -> str:
        number = (self.constants.today - self.constants.start_date).days
        if self.constants.today >= date(2022, 3, 30):
            number -= 1
        for i, cmp in enumerate(self.comparisons):
            if all([v.evaluation == Evaluation.correct for _, v in cmp.items()]):
                guesses_till_correct = str(i + 1)
                break
        else:
            guesses_till_correct = "X"
        return f"Wordle {number} {guesses_till_correct}/6\n"
