import logging

from flask import Blueprint, Response
from flask import request, render_template, redirect, url_for, flash
from flask_menu import register_menu

from .. import api

from ._utils import call


UNKNOWN_COLLECTION_NAME = "No Such Collection"

blueprint = Blueprint('collections', __name__)
log = logging.getLogger(__name__)


def _show_items():
    parts = [p for p in request.path.split('/') if p]
    return parts and parts[0] != 'collections'


def _activate_items():
    return not request.path.endswith('vote')


def _show_vote():
    return _show_items()


@blueprint.route("/collections/")
def index():
    content, status = call(api.collections.index)
    assert status == 200

    return Response(render_template("collections.html",
                                    collections=content['_items']))


@blueprint.route("/<code>")
@register_menu(blueprint, '.detail', "Items", order=1,
               visible_when=_show_items,
               active_when=_activate_items)
def detail(code):
    key = _get_key(code)

    content, status = call(api.scores.index, key=key)
    if status == 404:
        content['name'] = UNKNOWN_COLLECTION_NAME

    return Response(render_template("items.html", collection=content))


@blueprint.route("/<code>", methods=['POST'])
def append(code):
    key = _get_key(code)

    name = request.form['name'].strip()

    if name:
        _, status = call(api.items.add, key=key, name=name)
        assert status == 200

        flash(f"Added item: {name}", 'info')
    else:
        flash("A name is required.", 'danger')

    return redirect(url_for('collections.detail', code=code))


@blueprint.route("/<code>/vote", methods=['GET', 'POST'])
@register_menu(blueprint, '.vote', "Vote", order=2,
               visible_when=_show_items)
def vote(code):
    key = _get_key(code)

    if request.method == 'POST':
        winner = request.args.get('winner')
        loser = request.args.get('loser')

        content, status = call(api.votes.append, key=key,
                               winner=winner, loser=loser)

        return redirect(url_for('collections.vote', code=code))

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
