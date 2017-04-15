import logging

from flask import Blueprint, Markup
from flask import (request, render_template, send_file, redirect, url_for,
                   flash, abort)
from flask_menu import register_menu

from .. import api

from ._navbar import show_items, activate_items
from ._utils import call, create_csv, mark_pair_viewed, filter_viewed_pairs


blueprint = Blueprint('votes', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/<code>", strict_slashes=False)
@register_menu(blueprint, '.detail', "Results", order=2,
               visible_when=show_items,
               active_when=activate_items)
def results(code):
    key, slug = _get_key(code)
    if slug and code != slug:
        return redirect(url_for('votes.results', code=slug))

    content, status = call(api.scores.index, key=key)
    if status != 200:
        abort(404)

    return render_template("results.html", collection=content)


@blueprint.route("/<code>", methods=['POST'])
def add_item(code):
    key, _ = _get_key(code, require_unlocked=True)

    name = request.form['name'].strip()

    if name and key:
        content, status = call(api.items.add, key=key, name=name)
        if status == 200:
            item = content['_objects'][-1]
            flash(f"Added item: {item['name']}", 'info')
        else:
            flash(content['message'], 'danger')
    elif key:
        flash("A name is required.", 'danger')
    else:
        flash("Unable to add items.", 'danger')

    return redirect(url_for('votes.results', code=code))


@blueprint.route("/<code>/results.csv")
def download_results(code):
    key, _ = _get_key(code)

    content, status = call(api.scores.data, key=key)
    assert status == 200

    name = content['name'].replace(' ', '_')
    filename = f"{name}_Results.csv"
    path = create_csv(filename, content['data'])

    return send_file(path, mimetype='text/csv', as_attachment=True,
                     attachment_filename=filename, cache_timeout=0)


@blueprint.route("/<code>/vote", methods=['GET', 'POST'])
@register_menu(blueprint, '.vote', "Vote", order=3,
               visible_when=show_items)
def cast(code):
    key, slug = _get_key(code)
    if slug and code != slug:
        return redirect(url_for('votes.cast', code=slug))

    if request.method == 'POST':
        winner = request.args.get('winner')
        loser = request.args.get('loser')
        skip = request.args.get('skip')

        if not skip:
            content, status = call(api.votes.add, key=key,
                                   winner=winner, loser=loser)

        mark_pair_viewed(code, [winner, loser])

        return redirect(url_for('votes.cast', code=code))

    content, status = call(api.votes.index, key=key)

    if status != 200:
        abort(404)

    percent, collection = filter_viewed_pairs(content)

    if percent is None:
        percent = 100
        collection['item_data'] = [{'name': "---"}] * 2
        url = url_for('votes.results', code=code, _external=True)
        msg = Markup(
            "You have voted on every pair in this collection. "
            f"Go back to the results: <a href='{url}'>{url}</a>")
        flash(msg, 'warning')

    return render_template("vote.html", collection=collection, percent=percent)


def _get_key(code, *, require_unlocked=False):
    # TODO: considering making a separate API for this to avoid exposing details
    log.debug("Looking up key from code: %s", code)

    content, status = call(api.redirects.detail, start_slug=code)
    if status == 200:
        slug = content['end_slug']
        log.debug("Found redirect %r => %r", code, slug)
        return None, slug

    content, status = call(api.collections.detail, key=None, code=code)
    if status == 200:
        key = content['key']
        log.debug("Found key: %s", key)

        if require_unlocked:
            if content['locked']:
                log.error("Invalid action on locked collection: %s", key)
                return None, code

        return key, None

    log.warning("Unknown code: %s", code)
    return None, code
