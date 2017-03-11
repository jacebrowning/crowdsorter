import logging

from flask import Blueprint, url_for
from flask_api import status

from ..models import Collection

from ._schemas import parser, VoteSchema
from . import _exceptions as exceptions


blueprint = Blueprint('votes_api', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/api/collections/<key>/votes/")
def index(key):
    collection = Collection.objects(key=key).first()
    if not collection:
        raise exceptions.NotFound

    return serialize(collection), status.HTTP_200_OK


@blueprint.route("/api/collections/<key>/votes/", methods=['POST'])
@parser.use_kwargs(VoteSchema)
def add(key, winner, loser):
    collection = Collection.objects(key=key).first()
    if not collection:
        raise exceptions.NotFound

    log.debug("Comparison result: %s > %s", winner, loser)
    collection.vote(winner, loser)
    collection.save()

    return serialize(collection), status.HTTP_200_OK


@blueprint.route("/api/collections/<key>/votes/", methods=['DELETE'])
def clear(key):
    collection = Collection.objects(key=key).first()
    if not collection:
        raise exceptions.NotFound

    collection.votes.clear()
    collection.vote_count = 0
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
        code=collection.code,
        item_data=[serialize_item(i) for i in collection.items_by_confidence],
        vote_count=collection.vote_count,
    )


def serialize_item(item):
    return dict(
        name=item.name,
        description=item.description,
        image_url=item.image_url,
        ref_url=item.ref_url,
    )
