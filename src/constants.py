# from dataclass import dataclass
from datetime import date, timedelta

from answers import ANSWERS
from possibles import POSSIBLE_ANSWERS


STARTING_DATE = date(2021, 6, 19)
TODAY = date.today()


class Constants:
    answers: dict = {
        str(STARTING_DATE + timedelta(days=x)): y
        for x, y in enumerate(ANSWERS)
    }
    possibles: set = POSSIBLE_ANSWERS
    today: date = TODAY
    start_date: date = STARTING_DATE
