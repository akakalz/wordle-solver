import re
from regex_generator import Rules
from collections import Counter
from constants import ALPHA, VOWELS


class SmartGuesser:
    def __init__(self, rules: Rules, known_potentials: list, guesses_left: int) -> None:
        self.rules = rules
        self.known_potentials = known_potentials
        self.guesses_left = guesses_left

    def find_best_guess(self) -> str:
        # collapse all guesses into a Counter to find most/least common letters
        # possibly find most common patterns as well; sequentials??
        counter = self.create_counter()
        print(f"sg counter: {counter}")
        top_vowels = self.get_top_two_vowels_from_counter(counter)
        top_consonants = self.get_top_four_consonants(counter)
        test_rule = Rules()
        test_rule.must_haves = top_vowels.union(top_consonants)
        print(f"here: {test_rule.must_haves}")
        test_rule.dead_letters = ALPHA - test_rule.must_haves
        regex = re.compile(test_rule.generate_regex())
        print(regex)
        top_guesses = {
            x for x in self.known_potentials if regex.match(x)
        }
        iter_break = 5
        counts = 0
        while not top_guesses and counts < iter_break:
            top_vowels = top_vowels.union(self.get_top_two_vowels_from_counter(counter, excluded=top_vowels))
            test_rule.dead_letters = test_rule.dead_letters - top_vowels
            test_rule.must_haves = test_rule.must_haves.union(top_vowels)
            counts += 1
            if top_guesses:
                break
        else:
            # if all else fails, return an item from the potentials
            word = sorted(self.known_potentials).pop()
        if top_guesses:
            print(top_guesses)
            word = sorted(top_guesses, reverse=True).pop()
        print(f"smart guesser is using {word}")
        return word

    def create_counter(self) -> Counter:
        return Counter(
            "".join(self.known_potentials)
        )

    def get_top_two_vowels_from_counter(self, counter: Counter, excluded: set = None) -> set:
        if not excluded:
            excluded = set()
        vowels = [
            (k, v) for k, v in counter.items() if k in VOWELS and k not in excluded
        ]
        vowels = sorted(vowels, key=lambda x: x[1], reverse=True)
        if len(vowels) > 1:
            tie_breaks = vowels[1][1]
            vowels = sorted([x for x in vowels if x[1] >= tie_breaks], key=lambda x: x[0])
        return set(x[0] for x in vowels[:2])

    def get_top_four_consonants(self, counter: Counter) -> set:
        consonants = [
            (k, v) for k, v in counter.items() if k not in VOWELS
        ]
        consonants = sorted(consonants, key=lambda x: x[1], reverse=True)
        if len(consonants) > 3:
            tie_breaks = consonants[3][1]
            consonants = sorted([x for x in consonants if x[1] >= tie_breaks], key=lambda x: x[0])
        return set(x[0] for x in consonants[:4])
