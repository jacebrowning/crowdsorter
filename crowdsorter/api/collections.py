import logging

from flask import Blueprint, url_for, current_app
from flask_api import status

from ..models import Collection

from ._schemas import (parser, TokenSchema, CollectionSchema,
                       NewCollectionSchema, EditCollectionSchema)
from . import _exceptions as exceptions


blueprint = Blueprint('collections_api', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/api/collections/")
@parser.use_kwargs(TokenSchema)
def index(token, limit=None, **filter):
    if token != current_app.config['AUTH_TOKEN']:
        raise exceptions.PermissionDenied

    collections = Collection.objects(**filter) \
                            .order_by('-vote_count') \
                            .limit(limit)

    content = dict(
        _links=dict(
            root=url_for('root_api.index', _external=True),
            self=url_for('collections_api.index', _external=True),
        ),
        _items=[serialize(c) for c in collections]
    )

    return content, status.HTTP_200_OK


@blueprint.route("/api/collections/", methods=['POST'])
@parser.use_kwargs(NewCollectionSchema)
def create(name, code, items):
    collection = Collection(name=name, code=code, items=items)
    collection.save()

    return serialize(collection), status.HTTP_201_CREATED


@blueprint.route("/api/collections/<key>")
@parser.use_kwargs(CollectionSchema)
def detail(key, code):
    collection = None

    if code:
        collection = Collection.objects(code=code).first()

    if not collection:
        collection = Collection.objects(key=key).first()

    if not collection:
        raise exceptions.NotFound

    return serialize(collection), status.HTTP_200_OK


@blueprint.route("/api/collections/<key>", methods=['PUT'])
@parser.use_kwargs(EditCollectionSchema)
def update(key, name, owner, code, private, locked):
    collection = Collection.objects(key=key).first()

    if name:
        collection.name = name
    if owner:
        collection.owner = owner
    if code:
        collection.code = code
    if private is not None:
        collection.private = private
    if locked is not None:
        collection.locked = locked

    try:
        collection.save()
    except exceptions.NotUniqueError:
        msg = f"Short code is already taken: {collection.code}"
        raise exceptions.UnprocessableEntity(msg)
    except exceptions.ValidationError as exc:
        msg = list(exc.to_dict().values())[0]
        raise exceptions.UnprocessableEntity(msg)

    return serialize(collection), status.HTTP_200_OK


@blueprint.route("/api/collections/<key>", methods=['DELETE'])
def delete(key):
    collection = Collection.objects(key=key).first()
    if collection:
        log.info(f"Deleting: {collection!r}")
        collection.delete()
    else:
        log.warning(f"Already deleted: {collection!r}")

    return '', status.HTTP_204_NO_CONTENT


def serialize(collection):
    return dict(
        _links=dict(
            self=url_for('collections_api.detail', key=collection.key,
                         _external=True),
            items=url_for('items_api.index',
                          key=collection.key, _external=True),
            votes=url_for('votes_api.index',
                          key=collection.key, _external=True),
            scores=url_for('scores_api.index',
                           key=collection.key, _external=True),
        ),
        key=collection.key,
        name=collection.name,
        owner=collection.owner or '',
        code=collection.code,
        private=collection.private,
        locked=collection.locked,
        items=collection.items,
        vote_count=collection.vote_count,
    )
