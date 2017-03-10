import logging

from flask import Blueprint, url_for
from flask_api import status

from ..models import Collection, Item

from ._schemas import parser, ItemSchema
from ._serializers import serialize_item
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
@parser.use_kwargs(ItemSchema)
def add(key, name, **kwargs):
    collection = Collection.objects(key=key).first()
    if not collection:
        raise exceptions.NotFound

    log.debug("Adding to %r: %r", collection, name)
    collection.add(name, **kwargs)
    collection.save()

    return serialize(collection), status.HTTP_200_OK


@blueprint.route("/api/items/<key>")
def detail(key):
    item = Item.objects(key=key).first()
    if not item:
        raise exceptions.NotFound

    return serialize_item(item), status.HTTP_200_OK


@blueprint.route("/api/collections/<key>/items/<name>", methods=['DELETE'])
def remove(key, name):
    collection = Collection.objects(key=key).first()
    if not collection:
        raise exceptions.NotFound

    log.debug("Removing from %r: %r", collection, name)
    for item in collection.items:
        if item.name == name:
            collection.items.remove(item)
            collection.save()
            item.delete()
            break
    else:
        log.warning("No such item: %s", name)

    return sorted([i.name for i in collection.items]), status.HTTP_200_OK


def serialize(collection):
    return dict(
        _links=dict(
            self=url_for('items_api.index', key=collection.key, _external=True),
            collection=url_for('collections_api.detail',
                               key=collection.key, _external=True),
        ),
        _objects=[serialize_item(o) for o in collection.items],
    )
