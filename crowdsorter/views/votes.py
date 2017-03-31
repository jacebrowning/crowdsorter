import logging

from flask import Blueprint, Markup
from flask import request, render_template, redirect, url_for, flash, abort
from flask_menu import register_menu

from .. import api

from ._utils import call, parts, filter_pairs


blueprint = Blueprint('votes', __name__)
log = logging.getLogger(__name__)


def _show_items():
    return parts() and parts()[0] not in ['collections', 'items']


def _activate_items():
    return parts()[-1] != 'vote'


@blueprint.route("/<code>", strict_slashes=False)
@register_menu(blueprint, '.detail', "Results", order=2,
               visible_when=_show_items,
               active_when=_activate_items)
def results(code):
    key = _get_key(code)

    content, status = call(api.scores.index, key=key)
    if status != 200:
        abort(404)

    return render_template("results.html", collection=content)


@blueprint.route("/<code>", methods=['POST'])
def add_item(code):
    key = _get_key(code, require_unlocked=True)

    name = request.form['name'].strip()

    if name:
        content, status = call(api.items.add, key=key, name=name)
        if status == 200:
            item = content['_objects'][-1]
            flash(f"Added item: {item['name']}", 'info')
        else:
            flash("Unable to add items.", 'danger')
    else:
        flash("A name is required.", 'danger')

    return redirect(url_for('votes.results', code=code))


@blueprint.route("/<code>/vote", methods=['GET', 'POST'])
@register_menu(blueprint, '.vote', "Vote", order=3,
               visible_when=_show_items)
def cast(code):
    key = _get_key(code)

    if request.method == 'POST':
        winner = request.args.get('winner')
        loser = request.args.get('loser')

        content, status = call(api.votes.add, key=key,
                               winner=winner, loser=loser)

        return redirect(url_for('votes.cast', code=code))

    content, status = call(api.votes.index, key=key)

    if status != 200:
        abort(404)

    percent, collection = filter_pairs(content)

    if percent is None:
        percent = 100
        collection['items'] = ["---"] * 2
        url = url_for('votes.results', code=code, _external=True)
        msg = Markup(
            "You have voted on every pair in this collection. "
            f"Go back to the results: <a href='{url}'>{url}</a>")
        flash(msg, 'warning')

    return render_template("vote.html", collection=collection, percent=percent)


def _get_key(code, *, require_unlocked=False):
    # TODO: considering making a separate API for this to avoid exposing details
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
