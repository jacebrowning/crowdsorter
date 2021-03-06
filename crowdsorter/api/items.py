import logging

from flask import Blueprint, url_for, redirect
from flask_api import status

from ..models import Collection, Item

from ._schemas import parser, ItemSchema, UpdateItemSchema
from ._serializers import serialize_item
from . import _exceptions as exceptions


blueprint = Blueprint('items_api', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/api/collections/<key>/items/")
def index(key):
    collection = Collection.objects(key=key).first()
    if not collection:
        raise exceptions.NotFound

    return serialize(collection), status.HTTP_200_OK


@blueprint.route("/api/collections/<key>/items/", methods=['POST'])
@parser.use_kwargs(ItemSchema)
def add(key, name, **kwargs):
    collection = Collection.objects(key=key).first()
    if not collection:
        raise exceptions.NotFound

    log.debug("Adding to %r: %r", collection, name)
    try:
        collection.add(name, **kwargs)
    except ValueError as exc:
        raise exceptions.Conflict(str(exc))
    else:
        collection.save()

    return serialize(collection), status.HTTP_200_OK


@blueprint.route("/api/collections/<c_key>/items/<i_key>")
def nested_item_detail(c_key, i_key):
    collection = Collection.objects(key=c_key).first()
    if not collection:
        raise exceptions.NotFound

    if i_key not in collection:
        raise exceptions.NotFound

    return redirect(url_for('items_api.detail', key=i_key))


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


@blueprint.route("/api/items/<key>")
def detail(key):
    item = Item.objects(key=key).first()
    if not item:
        raise exceptions.NotFound

    return serialize_item(item), status.HTTP_200_OK


@blueprint.route("/api/items/<key>", methods=['PUT'])
@parser.use_kwargs(UpdateItemSchema)
def update(key, name, description, image_url, ref_url, enabled):
    item = Item.objects(key=key).first()

    if name and name.strip():
        item.name = name.strip()
    if description is not None:
        item.description = description.strip()
    if image_url is not None:
        item.image_url = image_url.strip() or None
    if ref_url is not None:
        item.ref_url = ref_url.strip() or None
    if enabled is not None:
        item.enabled = enabled

    try:
        item.save()
    except exceptions.ValidationError as exc:
        msg = list(exc.to_dict().values())[0]
        raise exceptions.UnprocessableEntity(msg)

    return serialize_item(item), status.HTTP_200_OK


@blueprint.route("/api/items/<key>", methods=['DELETE'])
def delete(key):
    item = Item.objects(key=key).first()

    if item is None:
        return '', status.HTTP_204_NO_CONTENT

    for collection in Collection.objects(items=item):
        log.info("Removing %r from %r...", item, collection)
        collection.items.remove(item)
        collection.save()

    if item:
        log.info("Deleting %r...", item)
        item.delete()

    return '', status.HTTP_204_NO_CONTENT


def serialize(collection):
    return dict(
        _links=dict(
            self=url_for('items_api.index', key=collection.key, _external=True),
            collection=url_for('collections_api.detail',
                               key=collection.key, _external=True),
        ),
        _objects=[serialize_item(o) for o in collection.items],
    )
