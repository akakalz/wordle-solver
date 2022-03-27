from copy import deepcopy
import re
from typing import Set
from regex_generator import Rules
from abstracts.guesser import Guesser
from research.findings import letter_counts_in_answers
from collections import Counter


class CourseOfAction:
    SEED_GUESS: int = 0
    RANDOM_GUESS: int = 1
    EXPLORATORY_GUESS: int = 2
    TARGETED_LETTERS_GUESS: int = 3


class ShrewdGuesser(Guesser):

    def guess(self) -> str:
        action = self.determine_course_of_action()
        if action == CourseOfAction.SEED_GUESS:
            shrewd_guess = self.seed_guess()
        elif action == CourseOfAction.RANDOM_GUESS:
            shrewd_guess = self.random_guess()
        elif action == CourseOfAction.EXPLORATORY_GUESS:
            shrewd_guess = self.exploratory_guess()
        elif action == CourseOfAction.TARGETED_LETTERS_GUESS:
            shrewd_guess = self.targeted_letters_guess()
        if not shrewd_guess:  # in case there was an error generating a guess
            shrewd_guess = self.random_guess()
        return shrewd_guess

    def get_known_incorrect_letters(self) -> Set:
        return self.rules.dead_letters

    def get_known_correct_letters(self) -> Set:
        return self.rules.must_haves

    def get_current_possible_guesses(self) -> Set:
        return self.get_possible_guesses(self.rules)

    def get_possible_guesses(self, rules: Rules) -> Set:
        pttrn = re.compile(rules.generate_regex())
        return {
            poss_answer for poss_answer in self.constants.possibles
            if all([
                pttrn.match(poss_answer) and poss_answer not in self.prior_guesses,
                all([must_have in poss_answer for must_have in rules.must_haves])
            ])
        }

    def generate_exploratory_rules(self) -> Rules:
        min_count = 6
        new_dead_letters = self.get_known_correct_letters().union(
            self.get_known_incorrect_letters()
        )
        temp_rules = deepcopy(self.rules)
        temp_rules.must_haves = set()
        temp_rules.right_indexes = {}
        temp_rules.wrong_indexes = {}
        temp_rules.preferred_letters = self.get_top_x_chars(min_count, new_dead_letters)
        temp_rules.dead_letters = new_dead_letters

        while True:
            if {
                x for x in self.get_possible_guesses(temp_rules)
                if all([v == 1 for v in Counter(x).values()])
            }:
                break
            min_count += 1
            temp_rules.preferred_letters = self.get_top_x_chars(min_count, new_dead_letters)

        return temp_rules

    def determine_course_of_action(self) -> int:
        if not self.prior_guesses:
            return CourseOfAction.SEED_GUESS
        elif len(self.prior_guesses) == 1 and (len(self.rules.right_indexes) + len(self.rules.wrong_indexes)) < 3:
            return CourseOfAction.EXPLORATORY_GUESS
        elif all([
            len(self.rules.right_indexes) in {3, 4},
            len(self.get_current_possible_guesses()) > (self.constants.max_guesses - len(self.prior_guesses)),
        ]):
            return CourseOfAction.TARGETED_LETTERS_GUESS
        return CourseOfAction.RANDOM_GUESS  # if all else fails, go rando!

    def seed_guess(self) -> str:
        print("seed guess")
        return "orate"

    def random_guess(self) -> str:
        """
        given a rules set, select a guess from the possible set at random
        """
        print("random guess")
        return self.get_current_possible_guesses().pop()

    def exploratory_guess(self) -> str:
        """
        given extant rules set, generate a new rules set that contains no known
        must have letters and select a guess from that possible set at random
        """
        print("exploratory guess")
        temp_rules = self.generate_exploratory_rules()
        return {
            x
            for x in self.get_possible_guesses(temp_rules)
            if all([v == 1 for v in Counter(x).values()])
        }.pop()

    def targeted_letters_guess(self) -> str:
        print("targeted letters guess")
        min_letters = 5
        possibles = set()
        while True:
            must_have_letters = self.get_top_x_chars(min_letters, self.rules.dead_letters.union(self.rules.must_haves))
            if not self.vowels_present(must_have_letters):
                must_have_letters.union({"e"})
            temp_rules = Rules()
            temp_rules.preferred_letters = must_have_letters
            possibles = {
                x for x in self.get_possible_guesses(temp_rules)
                if all([v == 1 for v in Counter(x).values()])
            }

            if possibles:
                break
            if min_letters > 26:
                break
            min_letters += 1
        if possibles:
            return possibles.pop()
        return None

    def get_top_x_chars(self, x: int, excludes: Set) -> Set:
        return set(
            [
                letter for letter in letter_counts_in_answers if all([
                    letter not in excludes
                ])
            ][:x]
        )

    def vowels_present(self, letters: Set) -> bool:
        return any([x in self.constants.vowels for x in letters])
