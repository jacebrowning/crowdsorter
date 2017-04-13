import logging

from flask import Blueprint, url_for
from flask_api import status

from ..models import Collection

from . import _exceptions as exceptions


blueprint = Blueprint('scores_api', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/api/collections/<key>/scores/")
def index(key):
    collection = Collection.objects(key=key).first()
    if not collection:
        raise exceptions.NotFound

    return serialize(collection), status.HTTP_200_OK


def serialize(collection):
    return dict(
        _links=dict(
            self=url_for('scores_api.index', key=collection.key,
                         _external=True),
            collection=url_for('collections_api.detail',
                               key=collection.key, _external=True),
        ),
        name=collection.name,
        code=collection.code,
        private=collection.private,
        locked=collection.locked,
        vote_count=collection.vote_count,
        item_data=[
            score.get_data(include_key=not collection.locked, include_meta=True)
            for score in collection.scores
        ],
    )
