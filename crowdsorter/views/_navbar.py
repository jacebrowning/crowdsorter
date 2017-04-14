from flask import request


def show_items():
    """Determine if the items tab should be shown."""
    return _parts() and _parts()[0] not in ['collections', 'items']


def activate_items():
    """Determine if the admin tab is selected."""
    return _parts()[-1] != 'vote'


def show_admin():
    """Determine if the admin tab should be shown."""
    return len(_parts()) == 2 and _parts()[0] == 'collections'


def activate_collections():
    """Determine if the admin tab is selected."""
    return _parts() and _parts()[-1] == 'collections'


def _parts():
    """Get the non-empty parts of the request path."""
    return [p for p in request.path.split('/') if p]
