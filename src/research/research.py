from answers import ANSWERS
from constants import ALPHA, Constants
from collections import Counter

# from shrewd_guesser import ShrewdGuesser
# from regex_generator import Rules

import json


def main() -> None:
    letter_counts = {
        x: 0 for x in ALPHA
    }
    for answer in ANSWERS:
        cntr = Counter(answer)
        for k, v in cntr.items():
            letter_counts[k] += v

    top_10 = sorted(
        [
            (k, v)
            for k, v in letter_counts.items()
        ],
        key=lambda x: x[1],
        reverse=True,
    )[:10]
    print(top_10)
    # top 10 letters in answers
    # [
    #   ('e', 1230),
    #   ('a', 975),
    #   ('r', 897),
    #   ('o', 753),
    #   ('t', 729),
    #   ('l', 716),
    #   ('i', 670),
    #   ('s', 668),
    #   ('n', 573),
    #   ('c', 475),
    # ]
    print(json.dumps(letter_counts))
    """
    {
        "e": 1230,
        "a": 975,
        "r": 897,
        "o": 753,
        "t": 729,
        "l": 716,
        "i": 670,
        "s": 668,
        "n": 573,
        "c": 475,
        "u": 466,
        "y": 424,
        "d": 393,
        "h": 387,
        "p": 365,
        "m": 316,
        "g": 310,
        "b": 280,
        "f": 229,
        "k": 210,
        "w": 194,
        "v": 152,
        "z": 40,
        "x": 37,
        "q": 29,
        "j": 27,
    }
    """
    letter_in_words_count = {
        x: 0 for x in ALPHA
    }
    for answer in ANSWERS:
        for k in letter_in_words_count:
            letter_in_words_count[k] += (1 if k in answer else 0)
    print(json.dumps(letter_in_words_count))
    """
    {
        "e": 1053,
        "a": 906,
        "r": 835,
        "o": 672,
        "t": 667,
        "i": 646,
        "l": 645,
        "s": 617,
        "n": 548,
        "u": 456,
        "c": 446,
        "y": 416,
        "h": 377,
        "d": 370,
        "p": 345,
        "g": 299,
        "m": 298,
        "b": 266,
        "f": 206,
        "k": 202,
        "w": 193,
        "v": 148,
        "x": 37,
        "z": 35,
        "q": 29,
        "j": 27
    }
    """


def main_2():
    c = Constants()
    for k, v in c.answers.items():
        if v == "harry":
            print(v, k)
            break
    # for k, v in c.answers.items():
    #     if k < str(c.today):
    #         print(v, k)
    # r = Rules()
    # sg = ShrewdGuesser(r, c, [])
    # print(sg.get_potential_answer_with_most_letters_from_set())



if __name__ == "__main__":
    main_2()
