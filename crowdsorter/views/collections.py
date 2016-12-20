import logging

from flask import Blueprint, Response
from flask import request, render_template, redirect, url_for
from flask_menu import register_menu

from .. import api

from ._utils import call


UNKNOWN_COLLECTION_NAME = "No Such Collection"

blueprint = Blueprint('collections', __name__)
log = logging.getLogger(__name__)


def _show_detail():
    return request.path not in ["/", "/collections"]


def _activate_detail():
    return 'vote' not in request.path.split('/')


def _show_vote():
    return request.path not in ["/", "/collections"]


@blueprint.route("/collections/")
def index():
    content, status = call(api.collections.index)
    assert status == 200

    return Response(render_template("collections.html",
                                    collections=content['_items']))


@blueprint.route("/<code>")
@blueprint.route("/collections/<key>")
@register_menu(blueprint, 'collections.detail', "Items", order=1,
               visible_when=_show_detail,
               active_when=_activate_detail)
def detail(code=None, key=None):
    if code:
        key = _get_key(code)

    content, status = call(api.scores.index, key=key)
    if status == 404:
        content['name'] = UNKNOWN_COLLECTION_NAME

    return Response(render_template("items.html", collection=content))


@blueprint.route("/<code>/vote", methods=['GET', 'POST'])
@blueprint.route("/collections/<key>/vote", methods=['GET', 'POST'])
@register_menu(blueprint, 'collections.vote', "Vote", order=2,
               visible_when=_show_vote)
def vote(code=None, key=None):
    if code:
        key = _get_key(code)
    else:
        log.debug("Key specified: %s", key)

    if request.method == 'POST':
        winner = request.args.get('winner')
        loser = request.args.get('loser')

        content, status = call(api.votes.append, key=key,
                               winner=winner, loser=loser)

        kwargs = dict(code=code) if code else dict(key=key)
        return redirect(url_for('collections.vote', **kwargs))

    content, status = call(api.votes.index, key=key)
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
