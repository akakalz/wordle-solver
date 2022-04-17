# import re
# from loguru import logger
from datetime import date, timedelta
from typing import List
from constants import Constants, MAX_GUESSES
from rules_generator import Rules
# from renderer import WordCompare, Renderer
from renderer import Evaluation, WordleCompare, WordleRenderer
# from smart_guesser import SmartGuesser
from shrewd_guesser import ShrewdGuesser


class Solver:
    def __init__(self, constants: Constants) -> None:
        self.constants = constants
        if self.constants.today > date.today():
            raise ValueError("it's not the future yet!")
        # `harry` day was skipped, so adding a day
        if self.constants.today >= date(2022, 3, 30):
            self._answer = self.constants.answers.get(str(self.constants.today + timedelta(days=1)))
        else:
            self._answer = self.constants.answers.get(str(self.constants.today))
        self._rules = Rules()
        self.guesses: List[WordleCompare] = []
        self.prior_answers: set = set(
            v for k, v in self.constants.answers.items() if str(k) < str(self.constants.today)
        )

    def play(self) -> int:
        while not self.is_solved() and len(self.guesses) < MAX_GUESSES:
            guesser = ShrewdGuesser(self._rules, self.constants, self.guesses)
            self._make_guess(guesser.guess())
        renderer = WordleRenderer(self.constants, [x.comparison for x in self.guesses])
        print(renderer.render())
        return len(self.guesses) if self.is_solved() else 10

    def _make_guess(self, word: str) -> None:
        print(f"guessing {word}")
        # logger.opt(colors=True).info(f"guessing <green>{word}</green>")
        guess = WordleCompare(word, self._answer)
        self.guesses.append(guess)
        self._rules.ingest_comparisons(guess.comparison)

    def is_solved(self) -> bool:
        if not self.guesses:
            return False
        return all([x.evaluation == Evaluation.correct for _, x in self.guesses[-1].comparison.items()])
