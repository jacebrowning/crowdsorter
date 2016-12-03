import logging

from bson.objectid import ObjectId

from ..extensions import db


log = logging.getLogger(__name__)


def generate_key():
    """Generate a MongoDB ObjectID-compatible string."""
    return str(ObjectId())


class Collection(db.Document):
    """Represents a named collection of items."""

    key = db.StringField(primary_key=True, default=generate_key)
    name = db.StringField()
    items = db.ListField(db.StringField())
