from abc import ABC, abstractmethod
from regex_generator import Rules
from constants import MAX_GUESSES


class Guesser(ABC):
    def __init__(
        self,
        rules: Rules,
        prior_guesses: list,
        max_guesses: int = MAX_GUESSES,
    ) -> None:
        self.rules = rules
        self.prior_guesses = prior_guesses
        self.max_guesses = max_guesses

    @abstractmethod
    def guess(self) -> str:
        ...
