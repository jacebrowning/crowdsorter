from flask import session


SESSION_VERSION = 1  # increment when session logic changes to clear sessions
SESSION_PREFIX_VIEWED_PAIRS = f"viewed-pairs:{SESSION_VERSION}:"


def get_viewed_pairs(code):
    key = SESSION_PREFIX_VIEWED_PAIRS + code
    viewed_pairs = session.get(key) or []
    return viewed_pairs


def set_viewed_pairs(code, viewed_pairs):
    key = SESSION_PREFIX_VIEWED_PAIRS + code
    session[key] = viewed_pairs
    session.permanent = True
