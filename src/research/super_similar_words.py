from collections import Counter
import re
from typing import Dict


class SuperSimilar:

    def __init__(self, words: set) -> None:
        self.words = words

        self.counts = self.get_letter_counts()
        self.two_thirds = 0.666667 * len(self.words)
        self._recommendations: set = None

    def has_super_similar(self) -> bool:
        if len(self.words) < 3:
            return False
        return self.count_similarities() and self.letter_position_similarities()

    def letter_position_similarities(self) -> bool:
        candidates = sorted(self.counts, key=lambda x: self.counts[x], reverse=True)[:4]
        pos = {x: [] for x in candidates}
        for word in self.words:
            for letter in pos:
                pos[letter].extend([i for i, c in enumerate(word) if c == letter])
        common_pos = {
            k: Counter(v)
            for k, v in pos.items()
        }
        cand_pos = {
            k: sk[0]
            for k, v in common_pos.items()
            for sk in v.most_common(1)
        }
        self.regex = self.build_similar_regex(cand_pos)
        self._setup_recs()
        return len([x for x in self.words if self.regex.match(x)]) >= self.two_thirds

    def count_similarities(self) -> bool:
        sims = len([k for k, v in self.counts.items() if self.two_thirds <= v])
        if sims >= 4:
            return True
        return False

    def get_letter_counts(self) -> dict:
        counts = {}
        for word in self.words:
            c = Counter(word)
            for k, v in c.items():
                if k not in counts:
                    counts[k] = v
                else:
                    counts[k] += v
        return counts

    def build_similar_regex(self, letter_pos: Dict[str, int]) -> re.Pattern:
        base = ["."] * 5
        for k, v in letter_pos.items():
            base[v] = k
        return re.compile("".join(base).replace(".", "(.)"))

    def _get_recommendations(self) -> set:
        return self._recommendations

    def _set_recommendations(self, recs) -> None:
        self._recommendations = recs

    def _setup_recs(self) -> None:
        recs = set()
        for word in self.words:
            if self.regex.match(word):
                recs.add(self.regex.match(word).group(1))
        self._recommendations = recs

    recommendations: set = property(_get_recommendations, _set_recommendations)
