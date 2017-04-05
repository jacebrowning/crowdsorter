from ..extensions import db


class Redirect(db.Document):
    """Represents a page redirect."""

    start_slug = db.StringField(primary_key=True)
    end_slug = db.StringField(null=False)
