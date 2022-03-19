import re
from typing import List
from constants import Constants, MAX_GUESSES
from regex_generator import Rules
from renderer import WordCompare, Renderer
from smart_guesser import SmartGuesser
from shrewd_guesser import ShrewdGuesser


class Solver:
    seed_words: list = [
        "clear",
        "point",
        "posit",
        "crane",
        "riots",
        "slate",
        "crate",
    ]

    def __init__(self, constants: Constants) -> None:
        self.constants = constants

        self._answer = self.constants.answers.get(str(self.constants.today))
        self._rules = Rules()
        self.guesses: List[WordCompare] = []
        self.prior_answers: set = set(
            v for k, v in self.constants.answers.items() if str(k) < str(self.constants.today)
        )

    def play(self) -> int:
        while not self.is_solved() and len(self.guesses) < MAX_GUESSES:
            sg = ShrewdGuesser(self._rules, self.guesses)
            self._make_guess(sg.guess())
        renderer = Renderer(self.constants, [x.comparison for x in self.guesses])
        print(renderer.render())
        return len(self.guesses) if self.is_solved() else 10

    def _make_guess(self, word: str) -> WordCompare:
        print(f"guessing {word}")
        guess = WordCompare(word, self._answer)
        self.guesses.append(guess)
        self._rules.ingest_comparison(guess.comparison)

    def initial_guess(self) -> None:
        self._make_guess(self.seed_words[0])

    def guess(self, guess_set: set) -> None:
        new_word = guess_set.pop()
        self._make_guess(new_word)

    def find_next_guesses(self) -> set:
        regex = re.compile(self._rules.generate_regex())
        possibles = {
            x for x in self.constants.possibles if regex.match(x) and all([y in x for y in self._rules.must_haves])
        }
        return possibles - self.prior_answers

    def is_solved(self) -> bool:
        if not self.guesses:
            return False
        return all([x.letter_in_correct_location for _, x in self.guesses[-1].comparison.items()])
