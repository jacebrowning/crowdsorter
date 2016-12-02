import logging

from ..extensions import db


log = logging.getLogger(__name__)


class Collection(db.Document):
    """Represents a room with card queues."""

    name = db.StringField()
