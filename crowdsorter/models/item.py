import logging
from pprint import pformat


log = logging.getLogger(__name__)


class Item(object):

    def __init__(self, name, *, score=0.0, _items=None):
        self.name = name
        self.wins = []
        self.score = score
        self._items = [] if _items is None else _items

    def __repr__(self):
        return "Item({self.name!r}, score={self.score:.2f})".format(self=self)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.score < other.score

    @property
    def losses(self):
        for item in self._items:
            if self in item.wins:
                yield item

    def calculate_score(self):
        for losing_item in self.wins:
            self.score += 1.0

            for inferred_losing_item in losing_item.wins:
                if inferred_losing_item not in self.wins:
                    self.score += 0.99

        for winning_item in self.losses:
            self.score -= 1.0

            for inferred_winning_item in winning_item.losses:
                if inferred_winning_item not in self.losses:
                    self.score -= 0.99


class Items(list):

    @classmethod
    def build(cls, names):
        items = cls()
        for name in names:
            item = Item(name, _items=items)
            items.append(item)
        return items

    @property
    def tree(self):
        data = {}
        for item in self:
            data[str(item)] = [str(i) for i in item.wins]
        return data

    def find(self, name):
        """Locate and return an Item by name."""
        for item in self:
            if item.name == name:
                return item
        raise IndexError("Could not find item {!r}".format(name))

    def normalize(self):
        """Remove extra win-loss pairs."""
        for item in self:
            for beat_item in item.wins:
                if item in beat_item.wins:
                    item.wins.remove(beat_item)
                    beat_item.wins.remove(item)
                    log.debug("Removed cancellation: %s = %s", item, beat_item)
                while item.wins.count(beat_item) > 1:
                    item.wins.remove(beat_item)
                    log.debug("Removed duplicate: %s > %s", item, beat_item)

        log.debug("Normalized tree:\n%s", pformat(self.tree))

    def calculate_scores(self):
        """Update item scores."""
        for item in self:
            item.calculate_score()
