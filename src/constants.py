# from dataclass import dataclass
from datetime import date, timedelta

from answers import ANSWERS
from possibles import POSSIBLE_ANSWERS


MAX_GUESSES = 6

STARTING_DATE = date(2021, 6, 19)  # date wordle started
TODAY = date.today()
# TODAY = date(2022, 3, 26)
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
VOWELS = {
    "a", "e", "i", "o", "u", "y"
}

DATED_ANSWERS: dict = {
    str(STARTING_DATE + timedelta(days=x)): y
    for x, y in enumerate(ANSWERS)
}
PREVIOUS_ANSWERS: set = {
    y
    for x, y in enumerate(ANSWERS)
    if (STARTING_DATE + timedelta(days=x)) < TODAY
}


class Constants:
    answers: dict = DATED_ANSWERS
    previous_answers: set = PREVIOUS_ANSWERS
    possibles: set = POSSIBLE_ANSWERS - PREVIOUS_ANSWERS
    today: date = TODAY
    start_date: date = STARTING_DATE
    vowels: set = VOWELS
    max_guesses: int = MAX_GUESSES
