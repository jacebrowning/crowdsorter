import random

from bson.objectid import ObjectId


ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789"


def generate_key():
    """Generate a MongoDB ObjectID-compatible string."""
    return str(ObjectId())


def generate_code():
    """Generate a URL-compatible short code."""
    return ''.join(random.choice(ALPHABET) for _ in range(10))
