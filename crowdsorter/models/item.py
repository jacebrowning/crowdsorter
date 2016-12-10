class Item(object):

    def __init__(self, name, score=0.0):
        self.name = name
        self.score = score

    def __repr__(self):
        return "Item({self.name!r}, score={self.score!r})".format(self=self)

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.score < other.score
