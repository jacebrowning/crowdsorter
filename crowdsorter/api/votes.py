import logging

from flask import Blueprint, request, url_for
from flask_api import status

from ..models import Collection

from . import _exceptions as exceptions


blueprint = Blueprint('votes_api', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/api/collections/<key>/votes")
def index(key):
    collection = Collection.objects(key=key).first()
    if not collection:
        raise exceptions.NotFound

    return serialize(collection), status.HTTP_200_OK


@blueprint.route("/api/collections/<key>/votes", methods=['POST'])
def append(key, winner=None, loser=None):
    collection = Collection.objects(key=key).first()
    if not collection:
        raise exceptions.NotFound

    winner = winner or request.data.get('winner')
    loser = loser or request.data.get('loser')
    if not (winner and loser):
        msg = "Winner and loser are required."
        raise exceptions.UnprocessableEntity(msg)

    log.debug("Comparison result: %s > %s", winner, loser)
    collection.vote(winner, loser)
    collection.save()

    return serialize(collection), status.HTTP_200_OK


def serialize(collection):
    return dict(
        _links=dict(
            self=url_for('votes_api.index', key=collection.key, _external=True),
            collection=url_for('collections_api.detail',
                               key=collection.key, _external=True),
        ),
        name=collection.name,
        items=collection.items_prioritized,
    )
