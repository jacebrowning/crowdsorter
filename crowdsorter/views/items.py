import logging

from flask import Blueprint, Response
from flask import render_template

from .. import api

from ._utils import call


blueprint = Blueprint('items', __name__, url_prefix="/items")
log = logging.getLogger(__name__)


@blueprint.route("/<key>", strict_slashes=False)
def detail(key):
    content, status = call(api.items.detail, key=key)
    assert status == 200

    return Response(render_template("item.html", item=content))
