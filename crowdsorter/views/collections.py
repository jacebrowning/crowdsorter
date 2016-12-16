import logging

from flask import Blueprint, Response
from flask import request, render_template, redirect, url_for
from flask_menu import register_menu

from .. import api

from ._utils import call


UNKNOWN_COLLECTION_NAME = "No Such Collection"

blueprint = Blueprint('collections', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/collections/")
def index():
    return redirect(url_for('index.get'))


@blueprint.route("/<code>")
@blueprint.route("/collections/<key>")
@register_menu(blueprint, '.detail', "Items", order=1,
               visible_when=lambda: request.path != "/",
               active_when=lambda: 'vote' not in request.path.split('/'))
def detail(code=None, key=None):
    if code:
        key = _get_key(code)

    content, status = call(api.scores.detail, key=key)
    if status == 404:
        content['name'] = UNKNOWN_COLLECTION_NAME

    return Response(render_template("items.html", collection=content))


@blueprint.route("/<code>/vote", methods=['GET', 'POST'])
@blueprint.route("/collections/<key>/vote", methods=['GET', 'POST'])
@register_menu(blueprint, '.vote', "Vote", order=2,
               visible_when=lambda: request.path != "/")
def vote(code=None, key=None):
    if code:
        key = _get_key(code)
    else:
        log.debug("Key specified: %s", key)

    if request.method == 'POST':
        winner = request.args['winner']
        loser = request.args['loser']

        content, status = call(api.votes.compare, key=key,
                               winner=winner, loser=loser)

        kwargs = dict(code=code) if code else dict(key=key)
        return redirect(url_for('collections.vote', **kwargs))

    content, status = call(api.votes.compare, key=key)
    if status == 404:
        content['name'] = UNKNOWN_COLLECTION_NAME
        content['items'] = ["---"] * 10

    return Response(render_template("vote.html", content=content))


def _get_key(code):
    log.debug("Looking up key from code: %s", code)
    content, status = call(api.collections.detail, key=None, code=code)

    if status == 200:
        key = content['key']
        log.debug("Found key: %s", key)
    else:
        log.warning("Unknown code: %s", code)
        key = None

    return key
