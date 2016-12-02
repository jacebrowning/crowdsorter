from flask import request
from flask_nav.elements import Navbar, View, Text

from .. import __project__
from ..extensions import nav

from . import index
from . import collections
from . import api_root
from . import api_collections


@nav.navigation()
def top():
    code = request.view_args.get('code')
    name = request.args.get('name')

    home = View("home", 'index.get')
    collection = View(code, 'collections.detail', code=code, name=name)
    _page_name = request.path.split('/')[-1]
    _page_endpoint = request.url_rule.endpoint
    page = View(_page_name, _page_endpoint, code=code)

    if code:
        if page.text in ['join', 'options']:
            items = [home, collection, page]
        else:
            items = [home, collection]
    else:
        items = [home]

    return Navbar(__project__, *items)
