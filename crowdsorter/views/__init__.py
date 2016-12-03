import logging

from flask import request
from flask_nav.elements import Navbar, View, Text

from .. import __project__
from ..extensions import nav

from . import index
from . import collections


log = logging.getLogger(__name__)


@nav.navigation()
def top():
    key = request.view_args.get('key')

    home = View("Home", 'index.get')
    collection = View("Collection", 'collections.detail', key=key)
    page = _get_page(request.path, request.url_rule.endpoint, key)

    if key:
        if page:
            items = [home, collection, page]
        else:
            items = [home, collection]
    else:
        items = [home]

    return Navbar(__project__, *items)


def _get_page(path, endpoint, key):
    paths = path.split('/')
    log.debug("Request path: %s", paths)

    if len(paths) > 3:
        text = paths[-1].capitalize()
        return View(text, endpoint, key=key)
    else:
        return None
