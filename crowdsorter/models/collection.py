import random
import logging

from bson.objectid import ObjectId

from ..extensions import db

from . import Items


log = logging.getLogger(__name__)


def generate_key():
    """Generate a MongoDB ObjectID-compatible string."""
    return str(ObjectId())


class Loss(db.EmbeddedDocument):
    """The number of times an item has lost a comparison."""

    loser = db.StringField()
    count = db.IntField()


class Wins(db.EmbeddedDocument):
    """Stores the result of comparisons to other items."""

    winner = db.StringField()
    against = db.EmbeddedDocumentListField(Loss)


class Score(db.EmbeddedDocument):
    """Stores the computed score for an item."""

    name = db.StringField()
    points = db.FloatField()
    confidence = db.FloatField()


class Collection(db.Document):
    """Represents a named collection of items."""

    key = db.StringField(primary_key=True, default=generate_key)
    name = db.StringField()
    items = db.ListField(db.StringField())
    votes = db.EmbeddedDocumentListField(Wins)
    scores = db.EmbeddedDocumentListField(Score)

    def __repr__(self):
        return "<collection: {self.key}>".format(self=self)

    def __lt__(self, other):
        return self.key < other.key

    @property
    def items_shuffled(self):
        items = self.items.copy()
        random.shuffle(items)
        return items

    @property
    def items_prioritized(self):
        scores = self.scores.copy()
        random.shuffle(scores)
        scores.sort(key=lambda x: x['confidence'])
        return [item['name'] for item in scores]

    def vote(self, winner, loser):
        """Apply a new vote and update the items order."""
        self._init()
        self._clean()
        wins = self._find_wins(self.votes, winner)
        loss = self._find_loss(wins, loser)
        loss.count += 1
        self._sort()

    def _init(self):
        """Add default comparison data for new items."""
        for winner in self.items:
            wins = self._find_wins(self.votes, winner)
            for loser in self.items:
                if loser != winner:
                    self._find_loss(wins, loser)

    def _clean(self):
        """Remove stale comparison for deleted items."""

    def _sort(self):
        """Sort the items list based on comparison data."""
        items = Items.build(self.items)

        for wins in self.votes:
            for loss in wins.against:
                items.add_pair(wins.winner, loss.loser, loss.count)

        items.sort(reverse=True)
        for index, item in enumerate(items):
            log.debug("Updated scores %s: %r", index, item)

        self.items = [str(item) for item in items]
        self.scores = []
        for item in items:
            score = Score(name=item.name,
                          points=item.score[0],
                          confidence=item.score[1])
            self.scores.append(score)

    @staticmethod
    def _find_wins(votes, name):
        for wins in votes:
            if wins.winner == name:
                return wins

        wins = Wins(winner=name)
        votes.append(wins)
        return wins

    @staticmethod
    def _find_loss(wins, name):
        for loss in wins.against:
            if loss.loser == name:
                return loss

        loss = Loss(loser=name, count=0)
        wins.against.append(loss)
        return loss
