import random
import logging

from bson.objectid import ObjectId

from ..extensions import db

from . import Items
from ._config import CONFIDENCE_FUZZ


ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789"


log = logging.getLogger(__name__)


def generate_key():
    """Generate a MongoDB ObjectID-compatible string."""
    return str(ObjectId())


def generate_code():
    """Generate a URL-compatible short code."""
    return ''.join(random.choice(ALPHABET) for _ in range(10))


class Loss(db.EmbeddedDocument):
    """The number of times an item has lost a comparison."""

    loser = db.StringField()
    count = db.IntField()

    def __repr__(self):
        return repr(dict([
            ('loser', self.loser),
            ('count', self.count)
        ]))


class Wins(db.EmbeddedDocument):
    """Stores the result of comparisons to other items."""

    winner = db.StringField()
    against = db.EmbeddedDocumentListField(Loss)

    def __repr__(self):
        return repr(dict([
            ('winner', self.winner),
            ('against', repr(self.against))
        ]))


class Score(db.EmbeddedDocument):
    """Stores the computed score for an item."""

    name = db.StringField()
    points = db.FloatField()
    confidence = db.FloatField()

    def __repr__(self):
        return repr(self.data)

    @property
    def data(self):
        return dict(
            name=self.name,
            points=self.points,
            confidence=self.confidence,
        )


class Collection(db.Document):
    """Represents a named collection of items."""

    key = db.StringField(primary_key=True, default=generate_key)
    name = db.StringField()
    code = db.StringField(null=False, unique=True, default=generate_code)

    # Options
    private = db.BooleanField(null=False, default=False)
    locked = db.BooleanField(null=False, default=False)

    # Input data
    items = db.ListField(db.StringField())

    # User data
    votes = db.EmbeddedDocumentListField(Wins)

    # Computed properties
    scores = db.EmbeddedDocumentListField(Score)
    vote_count = db.IntField(null=False, default=0)

    def __repr__(self):
        return f"<collection: {self.key}>"

    def __lt__(self, other):
        return self.key < other.key

    @property
    def item_count(self):
        return len(self.items)

    @property
    def items_prioritized(self):
        scores = self.scores.copy()
        scores.sort(key=self._fuzz_confidence)
        return [item['name'] for item in scores]

    @staticmethod
    def _fuzz_confidence(score):
        ratio = 1.0 - CONFIDENCE_FUZZ
        return (score['confidence'] + .01) * random.uniform(ratio, 1.0)

    def vote(self, winner, loser):
        """Apply a new vote and update the items order."""
        wins = self._find_wins(self.votes, winner)
        loss = self._find_loss(wins, loser)
        loss.count += 1
        self.vote_count += 1

    def clean(self):
        """Called automatically prior to saving."""
        self._clean_code()
        self._clean_items()
        vote_count = self._clean_votes()
        self.vote_count = vote_count
        self._clean_scores()

    def _clean_code(self):
        if not self.code:
            log.warning("Generating missing code for %s", self.name)
            self.code = generate_code()

    def _clean_items(self):
        """Sort the items and remove duplicates."""
        self.items = sorted(set(self.items))

    def _clean_votes(self):
        """Add default comparison data for new items and remove stale votes."""
        count = 0

        for winner in self.items:
            wins = self._find_wins(self.votes, winner)
            for loser in self.items:
                if loser != winner:
                    loss = self._find_loss(wins, loser)
                    count += loss.count

        for wins in list(self.votes):
            if wins.winner in self.items:
                for loss in list(wins.against):
                    if loss.loser not in self.items:
                        log.warning("Removing stale loss: %s", loss.loser)
                        wins.against.remove(loss)
            else:
                log.warning("Removing stale win: %s", wins.winner)
                self.votes.remove(wins)

        return count

    def _clean_scores(self):
        """Sort the items list based on comparison data."""
        items = Items.build(self.items)

        for wins in self.votes:
            for loss in wins.against:
                items.add_pair(wins.winner, loss.loser, loss.count)

        items.sort()
        for index, item in enumerate(items):
            log.debug("Updated scores %s: %r", index, item)

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
