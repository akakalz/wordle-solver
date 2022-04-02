from abc import ABC, abstractmethod
from regex_generator import Rules
from constants import Constants


class Guesser(ABC):
    def __init__(
        self,
        rules: Rules,
        constants: Constants,
        prior_guesses: list,
    ) -> None:
        self.rules = rules
        self.prior_guesses = prior_guesses
        self.constants = constants

    @abstractmethod
    def guess(self) -> str:
        ...
