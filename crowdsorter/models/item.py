class Item(object):

    def __init__(self, name, score=0.0):
        self.name = name
        self.wins = []
        self.losses = []
        self._initial_score = score

    def __repr__(self):
        return "Item({self.name!r}, score={self.score:.2f})".format(self=self)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.score < other.score

    @property
    def score(self):
        value = self._initial_score

        for lossing_item in self.wins:
            value += 1.0

            for inferred_losing_item in lossing_item.wins:
                if inferred_losing_item not in self.wins:
                    value += 0.99

        for winning_item in self.losses:
            value -= 1.0

            for inferred_winning_item in winning_item.losses:
                if inferred_winning_item not in self.losses:
                    value -= 0.99

        return value


class Items(list):

    def find(self, name):
        for item in self:
            if item.name == name:
                return item
        raise IndexError("Could not find item {!r}".format(name))
