from copy import deepcopy
import re
from typing import Set
from regex_generator import Rules
from abstracts.guesser import Guesser
from research.findings import letter_counts_in_answers, word_counts_per_letter
from super_similar_words import SuperSimilar
from collections import Counter
from constants import Constants


class CourseOfAction:
    SEED_GUESS: int = 0
    RANDOM_GUESS: int = 1
    EXPLORATORY_GUESS: int = 2
    TARGETED_LETTERS_GUESS: int = 3
    LAST_WORD_STANDING: int = 4


class ShrewdGuesser(Guesser):

    def __init__(self, rules: Rules, constants: Constants, prior_guesses: list) -> None:
        super().__init__(rules, constants, prior_guesses)
        self.possibles = self.get_current_possible_guesses()
        self.ssw = SuperSimilar(self.possibles)
        self.guesses_left = 5 - len(prior_guesses)

        if len(self.possibles) <= 10:
            print(self.possibles)
        if not self.possibles:
            print(self.rules)

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
        elif action == CourseOfAction.LAST_WORD_STANDING:
            shrewd_guess = self.solve_guess()
        if not shrewd_guess:  # in case there was an error generating a guess
            shrewd_guess = self.random_guess()
        return shrewd_guess

    def get_known_incorrect_letters(self) -> Set:
        return self.rules.dead_letters

    def get_known_correct_letters(self) -> Set:
        return self.rules.must_haves

    def get_current_possible_guesses(self) -> Set:
        return self.get_possible_guesses(self.rules)

    def get_possible_guesses_orig(self, rules: Rules) -> Set:
        pttrn = re.compile(rules.generate_regex())
        return {
            poss_answer for poss_answer in self.constants.possibles
            if all([
                pttrn.match(poss_answer) and poss_answer not in self.prior_guesses,
                all([must_have in poss_answer for must_have in rules.must_haves])
            ])
        }

    def get_possible_guesses(self, rules: Rules) -> Set:
        possibles = set()
        if not rules.letter_counts:
            return self.constants.possibles

        if rules.preferred_letters:
            for word in self.constants.possibles:
                if word in self.prior_guesses:
                    continue
                for letter in rules.preferred_letters:
                    if letter in word:
                        possibles.add(word)
                        break
        else:
            for word in self.constants.possibles:
                if word in self.prior_guesses:
                    continue

                counter = Counter(word)
                if all([
                    all([
                        l in counter and c <= counter[l]
                        for l, c in rules.letter_counts.items()
                    ]),
                    all([x not in word for x in rules.dead_letters]),
                    all([
                        x == word[idx]
                        for idx, letters in rules.right_indexes.items()
                        for x in letters
                    ]),
                    all([
                        x != word[idx]
                        for idx, letters in rules.wrong_indexes.items()
                        for x in letters
                    ]),
                ]):
                    possibles.add(word)
        return possibles

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
        print(temp_rules)
        temp_rules.letter_counts = {
            x: 1
            for x in temp_rules.preferred_letters
        }

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
        if len(self.possibles) == 1:
            return CourseOfAction.LAST_WORD_STANDING
        super_sim_words = self.ssw.has_super_similar()
        if super_sim_words:
            print("I've determined that most of the guesses left have super similar structure")
            print(self.ssw.words)
            print(f"I'm recommending these letters to try {self.ssw.recommendations}")
        if len(self.prior_guesses) == 1 and (len(self.rules.right_indexes) + len(self.rules.wrong_indexes)) < 3:
            return CourseOfAction.EXPLORATORY_GUESS
        elif super_sim_words and self.guesses_left > 1:
            return CourseOfAction.TARGETED_LETTERS_GUESS
        elif super_sim_words:
            print(
                f"but given that I have {self.guesses_left} guesses left and {len(self.possibles)} choices, "
                "I will guess at random."
            )
            return CourseOfAction.RANDOM_GUESS
        return CourseOfAction.RANDOM_GUESS  # if all else fails, go rando!

    def seed_guess(self) -> str:
        print("seed guess")
        word = self.get_potential_answer_with_most_letters_from_set()
        # return "orate"
        return word

    def random_guess(self) -> str:
        """
        given a rules set, select a guess from the possible set at random
        """
        print("random guess")
        return self.possibles.pop()

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

    def solve_guess(self):
        print("well there's only one word left, let's solve this puzzle!")
        return self.possibles.pop()

    def targeted_letters_guess(self) -> str:
        print("targeted letters guess")
        guess = self.get_valid_word_with_most_letters_from_set(self.ssw.recommendations)
        if guess is None:
            print(
                "After considering all the possibilities of a targeted letters "
                "guess, I came up with nothing.. I'll guess a random word "
                "from my possibles."
            )
            self.random_guess()  # if all else fails...
        return guess

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

    def get_valid_word_with_most_letters_from_set(self, letter_set: set) -> str:
        return_word = None
        most_letters_from_set = 0
        for word in self.constants.valids:
            letters_in_set = sum([1 for c in letter_set if c in word])
            if letters_in_set > most_letters_from_set:
                most_letters_from_set = letters_in_set
                return_word = word
            if most_letters_from_set in {5, len(letter_set)}:
                break  # no need to continue
        return return_word

    def get_potential_answer_with_most_letters_from_set(self) -> str:
        return_word = None
        most_letters_from_set = 0
        letter_set = {
            x
            for i, x in enumerate(word_counts_per_letter)
            if x not in self.rules.dead_letters and i < 6
        }
        for word in self.constants.possibles:
            letters_in_set = sum([1 for c in letter_set if c in word])
            if letters_in_set > most_letters_from_set:
                most_letters_from_set = letters_in_set
                return_word = word
            if most_letters_from_set in {5, len(letter_set)}:
                break  # no need to continue
        return return_word
