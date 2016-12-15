import logging
from collections import defaultdict


log = logging.getLogger(__name__)


class Item(object):

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
        # pylint: disable=unused-variable
        points, confidence = self.score
        pattern = "<item: {self.name!r} = {points:.1f} @ {confidence:.1f}>"
        return pattern.format(**locals())

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.score > other.score

    def __hash__(self):
        return hash(self.name)

    @property
    def score(self):
        points = 0.0
        confidences = []

        for item in self.opponents:
            wins = self.wins[item]
            losses = self.losses[item]
            total = wins + losses

            if wins > losses:
                ratio = wins / total
                points += ratio

            elif losses > wins:
                ratio = losses / total
                points -= ratio

            elif wins or losses:
                ratio = 0.5

            else:
                ratio = 0.0

            confidences.append(ratio)

        if confidences:
            confidence = sum(confidences) / len(confidences)
        else:
            confidence = self._confidence or 0.0

        return self._points or points, self._confidence or confidence


class Items(list):

    @classmethod
    def build(cls, names):
        items = cls()

        for name in names:
            items.get_item(name)

        for this in items:
            for that in items:
                if this != that:
                    this.opponents.append(that)

        return items

    def add_pair(self, winner, loser, count=1):
        winning_item = self.get_item(winner)
        losing_item = self.get_item(loser)
        winning_item.wins[losing_item] += count
        losing_item.losses[winning_item] += count

    def get_item(self, name):
        for item in self:
            if item.name == name:
                return item

        item = Item(name)
        self.append(item)
        return item

    def get_names(self):
        return [item.name for item in self]
