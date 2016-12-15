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


@blueprint.route("/collections/<key>")
@register_menu(blueprint, '.detail', "Items", order=1,
               visible_when=lambda: 'collections' in request.path.split('/'),
               active_when=lambda: 'vote' not in request.path.split('/'))
def detail(key):
    content, status = call(api.scores.detail, key=key)
    if status == 404:
        content['name'] = UNKNOWN_COLLECTION_NAME

    return Response(render_template("items.html", collection=content))


@blueprint.route("/collections/<key>/vote", methods=['GET', 'POST'])
@register_menu(blueprint, '.vote', "Vote", order=2,
               visible_when=lambda: 'collections' in request.path.split('/'))
def vote(key):
    if request.method == 'POST':

        log.debug("Request args: %s", request.args)
        winner = request.args['winner']
        loser = request.args['loser']

        content, status = call(api.votes.compare, key=key,
                               winner=winner, loser=loser)

        return redirect(url_for('collections.vote', key=key))

    content, status = call(api.votes.compare, key=key)
    if status == 404:
        content['name'] = UNKNOWN_COLLECTION_NAME
        content['items'] = ["---"] * 10

    return Response(render_template("vote.html", content=content))
