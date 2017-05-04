import logging
from collections import defaultdict


INFERRED_POINTS_IMPACT = 0.9
INFERRED_RATIO_IMPACT = 0.9

log = logging.getLogger(__name__)


class Result(object):

    def __init__(self, item, *, _points=None, _confidence=None):
        self.item = item
        # Attributes set via the factory:
        self.opponents = []
        self.wins = defaultdict(int)
        self.losses = defaultdict(int)
        # Internal attributes used for testing:
        self._points = _points
        self._confidence = _confidence

    def __repr__(self):
        points, confidence = self.score
        return f"<item: '{self.item}' = {points:.3f} @ {confidence:.3f}>"

    def __str__(self):
        return f"{self.item}"

    def __eq__(self, other):
        return self.item == other.item

    def __ne__(self, other):
        return self.item != other.item

    def __gt__(self, other):
        return self.score > other.score

    def __hash__(self):
        return hash(self.item)

    @property
    def inferred_points_impact(self):
        count = len(self.opponents) + 1
        if count <= 2:
            return 0.0
        inferred_votes = ((count - 1) * (count - 2)) / 2
        return 1 / inferred_votes

    @property
    def score(self):
        total_points = 0.0
        ratios = []

        for opponent in self.opponents:

            points, ratio = self._get_score(self, opponent)
            total_points += points
            ratios.append(ratio)

            for inferred_opponent in opponent.opponents:

                inferred_points, ratio = self._get_score(opponent,
                                                         inferred_opponent)

                if inferred_points == 0.0:
                    continue
                if points >= 0.0 and inferred_points < 0.0:
                    continue
                if points <= 0.0 and inferred_points > 0.0:
                    continue

                total_points += inferred_points * self.inferred_points_impact
                ratios.append(ratio)

        if ratios:
            confidence = sum(ratios) / len(ratios)
        else:
            confidence = self._confidence or 0.0

        return self._points or total_points, self._confidence or confidence

    @staticmethod
    def _get_score(item, opponent):
        assert item != opponent

        wins = item.wins[opponent]
        losses = item.losses[opponent]
        total = wins + losses

        if wins > losses:
            ratio = wins / total
            points = ratio

        elif losses > wins:
            ratio = losses / total
            points = -ratio

        else:
            ratio = 0.0
            points = 0.0

        return points, ratio


class Results(list):

    @classmethod
    def build(cls, items):
        results = cls()

        for item in items:
            results.find(item, create=True)

        for this in results:
            for that in results:
                if this != that:
                    this.opponents.append(that)

        return results

    def find(self, item, create=False):
        for score in self:
            if score.item == item:
                return score

        if create:
            result = Result(item)
            self.append(result)
            return result

        log.warning("Unknown item: %s", item)
        return None

    def add_pair(self, winner, loser, count=1):
        winning_item = self.find(winner)
        losing_item = self.find(loser)
        if winning_item and losing_item:
            winning_item.wins[losing_item] += count
            losing_item.losses[winning_item] += count
