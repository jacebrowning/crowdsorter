import logging
from collections import defaultdict


log = logging.getLogger(__name__)


class Item(object):

    INFERRED_POINTS_IMPACT = 0.9
    INFERRED_RATIO_IMPACT = 0.5

    def __init__(self, name, *, _points=None, _confidence=None):
        self.name = name
        # Attributes set via the factory:
        self.opponents = []
        self.wins = defaultdict(int)
        self.losses = defaultdict(int)
        # Internal attributes used for testing:
        self._points = _points
        self._confidence = _confidence

    def __repr__(self):
        points, confidence = self.score
        return f"<item: {self.name!r} = {points:.1f} @ {confidence:.1f}>"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __lt__(self, other):
        return self.score > other.score

    def __hash__(self):
        return hash(self.name)

    @property
    def score(self):
        total_points = 0.0
        ratios = []

        for opponent in self.opponents:

            points, ratio = self._get_score(self, opponent)
            if (points, ratio) == (0.0, 0.0):
                for item, count in self.wins.items():
                    if not count:
                        continue
                    i_points, i_ratio = self._get_score(item, opponent)
                    if i_points > 0 and i_ratio > ratio:
                        points, ratio = i_points, i_ratio
                        points, ratio = i_points, i_ratio
                for item, count in self.losses.items():
                    if not count:
                        continue
                    i_points, i_ratio = self._get_score(item, opponent)
                    if i_points < 0 and i_ratio > ratio:
                        points, ratio = i_points, i_ratio

                points *= self.INFERRED_POINTS_IMPACT
                ratio *= self.INFERRED_RATIO_IMPACT

            total_points += points
            ratios.append(ratio)

        if ratios:
            confidence = sum(ratios) / len(ratios)
        else:
            confidence = self._confidence or 0.0

        return self._points or total_points, self._confidence or confidence

    @staticmethod
    def _get_score(item, opponent):
        if item == opponent:
            return 0, 0
        assert item != opponent, (item, opponent)
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


class Items(list):

    @classmethod
    def build(cls, names):
        items = cls()

        for name in names:
            items.find(name, create=True)

        for this in items:
            for that in items:
                if this != that:
                    this.opponents.append(that)

        return items

    def find(self, name, create=False):
        for item in self:
            if item.name == name:
                return item

        if create:
            item = Item(name)
            self.append(item)
            return item
        else:
            log.warning("Unknown item: %s", name)
            return None

    def add_pair(self, winner, loser, count=1):
        winning_item = self.find(winner)
        losing_item = self.find(loser)
        if winning_item and losing_item:
            winning_item.wins[losing_item] += count
            losing_item.losses[winning_item] += count
