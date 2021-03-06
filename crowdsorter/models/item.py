from ..extensions import db

from ._utils import generate_key


class Item(db.Document):

    key = db.StringField(primary_key=True, default=generate_key)

    name = db.StringField()
    description = db.StringField()
    image_url = db.URLField()
    ref_url = db.URLField()

    enabled = db.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"<item: {self.key}>"

    def __lt__(self, other):
        return self.key < other.key
