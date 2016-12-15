import logging
from collections import defaultdict


log = logging.getLogger(__name__)


class Item(object):

    def __init__(self, name, *, _points=None, _confidence=None):
        self.name = name
        self.win_count = defaultdict(int)
        self.loss_count = defaultdict(int)
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
        points = self._points or 0.0
        confidences = defaultdict(float)

        for item in self.win_count:
            wins = self.win_count[item]
            losses = self.loss_count[item]

            try:
                ratio = wins / (wins + losses)
            except ZeroDivisionError:
                ratio = 0.0

            points += 1.0 * ratio
            confidences[item] = max(confidences[item], ratio)

        for item in self.loss_count:
            losses = self.loss_count[item]
            wins = self.win_count[item]

            try:
                ratio = losses / (losses + wins)
            except ZeroDivisionError:
                ratio = 0.0

            points -= 1.0 * ratio
            confidences[item] = max(confidences[item], ratio)

        if confidences:
            confidence = sum(confidences.values()) / len(confidences)
        else:
            confidence = self._confidence or 0.0

        return points, confidence


class Items(list):

    @classmethod
    def build(cls, names):
        items = cls()

        for name in names:
            items.get_item(name)

        for item in items:
            for item2 in items:
                if item != item2:
                    item.win_count[item2] = 0
                    item.loss_count[item2] = 0

        return items

    def add_pair(self, winner, loser, count=1):
        winning_item = self.get_item(winner)
        losing_item = self.get_item(loser)
        winning_item.win_count[losing_item] += count
        losing_item.loss_count[winning_item] += count

    def get_item(self, name):
        for item in self:
            if item.name == name:
                return item

        item = Item(name)
        self.append(item)
        return item

    def get_names(self):
        return [item.name for item in self]
