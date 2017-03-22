import random
from datetime import datetime
import logging

from ..extensions import db

from . import Item, Results
from ._utils import generate_key, generate_code


log = logging.getLogger(__name__)


class Loss(db.EmbeddedDocument):
    """The number of times an item has lost a comparison."""

    loser = db.ReferenceField(Item)
    count = db.IntField()

    def __repr__(self):
        return repr(dict([
            ('loser', self.loser),
            ('count', self.count)
        ]))


class Wins(db.EmbeddedDocument):
    """Stores the result of comparisons to other items."""

    winner = db.ReferenceField(Item)
    against = db.EmbeddedDocumentListField(Loss)

    def __repr__(self):
        return repr(dict([
            ('winner', self.winner),
            ('against', repr(self.against))
        ]))


class Score(db.EmbeddedDocument):
    """Stores the computed score for an item."""

    item = db.ReferenceField(Item)
    points = db.FloatField()
    confidence = db.FloatField()

    def __repr__(self):
        return repr(self.data)

    @property
    def data(self):
        return dict(
            name=self.item.name,
            points=self.points,
            confidence=self.confidence,
        )


class Collection(db.Document):
    """Represents a named collection of items."""

    key = db.StringField(primary_key=True, default=generate_key)
    name = db.StringField()
    owner = db.EmailField()
    code = db.StringField(null=False, unique=True, default=generate_code)

    # Options
    private = db.BooleanField(null=False, default=False)
    locked = db.BooleanField(null=False, default=False)

    # Input data
    items = db.ListField(db.ReferenceField(Item))

    # User data
    votes = db.EmbeddedDocumentListField(Wins)

    # Computed properties
    date_voted = db.DateTimeField(default=datetime.now)
    vote_count = db.IntField(null=False, default=0)
    vote_count_decayed = db.FloatField(null=False, default=0.0)
    scores = db.EmbeddedDocumentListField(Score)

    # Metadata
    meta = {'indexes': [
        {
            'fields': ['$name'],
            'default_language': 'english',
            'weights': {'name': 1},
        },
    ]}

    def __repr__(self):
        return f"<collection: {self.key}>"

    def __str__(self):
        return f"{self.name}"

    def __lt__(self, other):
        return self.key < other.key

    def __contains__(self, other):
        if isinstance(other, Item):
            return other in self.items

        return other in [item.key for item in self.items]

    @property
    def item_count(self):
        return len(self.items)

    @property
    def items_by_confidence(self):
        scores = self.scores.copy()
        random.shuffle(scores)
        return [s.item for s in sorted(scores, key=lambda s: s.confidence)]

    def add(self, name, *, _save=True, **kwargs):
        """Add a new item and save it."""
        item = Item(name=name, **kwargs)

        if _save:
            item.save()

        self.items.append(item)

        return item

    def vote(self, winner, loser, *, _at=None):
        """Apply a new vote and update the items order."""
        # TODO: find the correct way to do this
        if isinstance(winner, str):
            for item in self.items:
                if item.name == winner:
                    winner = item
                    break
            else:
                log.warning("Unknown winner: %s", winner)
                return
        if isinstance(loser, str):
            for item in self.items:
                if item.name == loser:
                    loser = item
                    break
            else:
                log.warning("Unknown loser: %s", loser)
                return

        wins = self._find_wins(self.votes, winner)
        loss = self._find_loss(wins, loser)

        loss.count += 1
        self.vote_count += 1
        self.date_voted = _at or datetime.now()
        self._decay_votes()

    def _decay_votes(self):
        """Computed the decayed vote total based on the last-voted date."""
        delta = datetime.now() - self.date_voted
        ratio = 1 - (delta.days / 21)
        self.vote_count_decayed = round(self.vote_count * ratio, 3)

    def clean(self):
        """Called automatically prior to saving."""
        self._clean_code()
        vote_count = self._clean_votes()
        self.vote_count = vote_count
        self._decay_votes()
        self._clean_scores()

    def _clean_code(self):
        if not self.code:
            log.warning("Generating missing code for %s", self.name)
            self.code = generate_code()

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
        results = Results.build(self.items)

        for wins in self.votes:
            for loss in wins.against:
                results.add_pair(wins.winner, loss.loser, loss.count)

        results.sort()
        for index, result in enumerate(results):
            log.debug("Updated scores %s: %r", index, result)

        self.scores = []
        for result in results:
            score = Score(item=result.item,
                          points=result.score[0],
                          confidence=result.score[1])
            self.scores.append(score)

    @staticmethod
    def _find_wins(votes, item):
        for wins in votes:
            if wins.winner == item:
                return wins

        wins = Wins(winner=item)
        votes.append(wins)
        return wins

    @staticmethod
    def _find_loss(wins, item):
        for loss in wins.against:
            if loss.loser == item:
                return loss

        loss = Loss(loser=item, count=0)
        wins.against.append(loss)
        return loss
