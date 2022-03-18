# from dataclass import dataclass
from datetime import date, timedelta

from answers import ANSWERS
from possibles import POSSIBLE_ANSWERS


STARTING_DATE = date(2021, 6, 19)  # date wordle started
TODAY = date.today()
# TODAY = date(2022, 1, 1)
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


class Constants:
    answers: dict = {
        str(STARTING_DATE + timedelta(days=x)): y
        for x, y in enumerate(ANSWERS)
    }
    possibles: set = POSSIBLE_ANSWERS
    today: date = TODAY
    start_date: date = STARTING_DATE
