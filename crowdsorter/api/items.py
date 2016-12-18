import logging

from flask import Blueprint, request, url_for
from flask_api import status

from ..models import Collection

from . import _exceptions as exceptions


blueprint = Blueprint('items_api', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/api/collections/<key>/items")
def index(key):
    collection = Collection.objects(key=key).first()
    if not collection:
        raise exceptions.NotFound

    return serialize(collection), status.HTTP_200_OK


@blueprint.route("/api/collections/<key>/items", methods=['POST'])
def append(key, name=None):
    collection = Collection.objects(key=key).first()
    if not collection:
        raise exceptions.NotFound

    name = name or request.data.get('name')
    if not name:
        raise exceptions.UnprocessableEntity("Name is required.")

    log.debug("Adding to %r: %r", collection, name)
    collection.items.append(name)
    collection.save()

    return serialize(collection), status.HTTP_200_OK


def serialize(collection):
    return dict(
        _links=dict(
            self=url_for('.index', key=collection.key, _external=True),
            collection=url_for('collections_api.detail',
                               key=collection.key, _external=True),
        ),
        items=collection.items,
    )
