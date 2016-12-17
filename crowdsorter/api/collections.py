import logging

from flask import Blueprint, request, url_for
from flask_api import status

from ..models import Collection

from . import _exceptions as exceptions


blueprint = Blueprint('collections_api', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/api/collections/")
def index():
    collections = sorted(Collection.objects)

    content = [url_for('collections_api.detail', key=c.id, _external=True)
               for c in collections]

    return content, status.HTTP_200_OK


@blueprint.route("/api/collections/", methods=['POST'])
def create():
    name = request.data.get('name')
    code = request.data.get('code')
    try:
        items = request.data.getlist('items')
    except AttributeError:
        # TODO: figure out how to test this automatically
        # it only seems to get triggered from the Flask-API browser
        items = request.data.get('items', [])
    if not name:
        raise exceptions.UnprocessableEntity("Name is required.")

    collection = Collection(name=name, code=code, items=items)
    collection.save()

    return serialize(collection), status.HTTP_201_CREATED


@blueprint.route("/api/collections/<key>")
def detail(key, code=None):
    collection = None

    code = code or request.args.get('code')
    if code:
        collection = Collection.objects(code=code).first()

    if not collection:
        collection = Collection.objects(key=key).first()

    if not collection:
        raise exceptions.NotFound

    return serialize(collection), status.HTTP_200_OK


@blueprint.route("/api/collections/<key>", methods=['POST'])
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
        uri=url_for('collections_api.detail',
                    key=collection.key, _external=True),
        key=collection.key,
        name=collection.name,
        code=collection.code,
        items=collection.items
    )
