import time
import logging

from flask import Blueprint, Response
from flask import (request, render_template, redirect, url_for, flash,
                   current_app, session)
from flask_menu import register_menu

from .. import api

from ._utils import call, parts


UNKNOWN_COLLECTION_NAME = "No Such Collection"
UNKNOWN_COLLECTION_CODE = "unknown"

blueprint = Blueprint('collections', __name__)
log = logging.getLogger(__name__)


def _activate_collections():
    return parts() and parts()[-1] == 'collections'


def _show_items():
    return parts() and parts()[0] != 'collections'


def _activate_items():
    return parts()[-1] != 'vote'


@blueprint.route("/collections/")
@register_menu(blueprint, '.index', "Collections", order=1,
               active_when=_activate_collections)
def index():
    content, status = call(api.collections.index, private=False, limit=15,
                           token=current_app.config['AUTH_TOKEN'])
    assert status == 200

    return Response(render_template("collections.html",
                                    collections=content['_items']))


@blueprint.route("/collections/", methods=['POST'])
def new():
    name = request.form.get('name', "").strip()

    if not name:
        flash("A name is required.", 'danger')
        return redirect(url_for('collections.index'))

    content, status = call(api.collections.create, name=name)
    assert status == 201

    flash(f"Created collection: {content['name']}", 'info')

    return redirect(url_for('admin.detail', key=content['key']))


@blueprint.route("/<code>", strict_slashes=False)
@register_menu(blueprint, '.detail', "Results", order=2,
               visible_when=_show_items,
               active_when=_activate_items)
def detail(code):
    key = _get_key(code)

    content, status = call(api.scores.index, key=key)
    if status == 404:
        content['name'] = UNKNOWN_COLLECTION_NAME
        content['code'] = code
        content['locked'] = True

    return Response(render_template("items.html", collection=content))


@blueprint.route("/<code>", methods=['POST'])
def add(code):
    key = _get_key(code, require_unlocked=True)

    name = request.form['name'].strip()

    if name:
        content, status = call(api.items.add, key=key, name=name)
        if status == 200:
            flash(f"Added item: {name}", 'info')
        else:
            flash("Unable to add items.", 'danger')
    else:
        flash("A name is required.", 'danger')

    return redirect(url_for('collections.detail', code=code))


@blueprint.route("/<code>/vote", methods=['GET', 'POST'])
@register_menu(blueprint, '.vote', "Vote", order=3,
               visible_when=_show_items)
def vote(code):
    key = _get_key(code)

    if request.method == 'POST':
        winner = request.args.get('winner')
        loser = request.args.get('loser')

        content, status = call(api.votes.add, key=key,
                               winner=winner, loser=loser)

        return redirect(url_for('collections.vote', code=code))

    content, status = call(api.votes.index, key=key)
    if status == 404:
        content['name'] = UNKNOWN_COLLECTION_NAME
        content['code'] = UNKNOWN_COLLECTION_CODE
        content['items'] = ["---"] * 10

    _removed_recently_viewed_items(content)

    return Response(render_template("vote.html", collection=content))


def _get_key(code, *, require_unlocked=False):
    log.debug("Looking up key from code: %s", code)
    content, status = call(api.collections.detail, key=None, code=code)

    if status == 200:
        key = content['key']
        log.debug("Found key: %s", key)

        if require_unlocked:
            if content['locked']:
                log.error("Invalid action on locked collection: %s", key)
                return None

        return key

    log.warning("Unknown code: %s", code)
    return None


def _removed_recently_viewed_items(content):
    voted = session.get('voted') or []
    names = content['items']

    for pair in voted:
        for name in pair:
            if len(names) <= 2:
                break
            if name == names[0]:
                names.pop(0)

    if len(names) >= 2:
        pair = names[0], names[1]
        voted.append(pair)

    while len(voted) > 10:
        voted.pop(0)

    session['voted'] = voted
    content['items'] = names

    return content
