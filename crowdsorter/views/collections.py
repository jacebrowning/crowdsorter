import logging

from flask import Blueprint, Response
from flask import request, render_template, redirect, url_for

from .. import api

from ._utils import call


blueprint = Blueprint('collections', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/collections/")
def index():
    return redirect(url_for('index.get'))


@blueprint.route("/collections/<key>")
def detail(key):
    content, status = call(api.collections.detail, key=key)
    assert status == 200

    return Response(render_template("collection.html", collection=content))


@blueprint.route("/collections/<key>/items")
def items(key):
    content, status = call(api.collections.detail, key=key)
    assert status == 200

    return Response(render_template("items.html", collection=content))


@blueprint.route("/collections/<key>/sort", methods=['GET', 'POST'])
def sort(key):
    if request.method == 'POST':

        log.debug("Request args: %s", request.args)
        winner = request.args['winner']
        loser = request.args['loser']

        content, status = call(api.collections.compare, key=key,
                               winner=winner, loser=loser)
        assert status == 200

        return redirect(url_for('collections.sort', key=key))

    content, status = call(api.collections.compare, key=key)
    assert status == 200

    return Response(render_template("sort.html", content=content))
