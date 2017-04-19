from flask import session


VERSION = 1  # increment when session logic changes to clear sessions
VOTED_NAMES = f"voted-names:{VERSION}:"
SKIPPED_NAMES = f"skipped-names:{VERSION}:"
VIEWED_PAIRS = f"viewed-pairs:{VERSION}:"


def get_voted_names(code):
    return _get(VOTED_NAMES, code)


def set_voted_names(code, names):
    _set(VOTED_NAMES, code, names)


def add_voted_name(code, name):
    names = get_voted_names(code)
    if name not in names:
        names.append(name)
        set_voted_names(code, names)


def get_skipped_names(code):
    return _get(SKIPPED_NAMES, code)


def set_skipped_names(code, names):
    _set(SKIPPED_NAMES, code, names)


def add_skipped_name(code, name):
    names = get_skipped_names(code)
    if name not in names:
        names.append(name)
        set_skipped_names(code, names)


def get_viewed_pairs(code):
    return _get(VIEWED_PAIRS, code)


def set_viewed_pairs(code, pairs):
    _set(VIEWED_PAIRS, code, pairs)


def add_viewed_pair(code, pair):
    pairs = get_viewed_pairs(code)
    if pair not in pairs:
        pairs.append(pair)
        set_viewed_pairs(code, pairs)


def _get(prefix, code):
    key = prefix + code
    value = session.get(key) or []
    return value


def _set(prefix, code, value):
    key = prefix + code
    session[key] = value
    session.permanent = True
