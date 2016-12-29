import logging

from flask import Blueprint, request, url_for, current_app
from flask_api import status

from ..models import Collection

from . import _exceptions as exceptions


blueprint = Blueprint('collections_api', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/api/collections/")
def index(token=None):
    token = token or request.args.get('token')
    if token != current_app.config['AUTH_TOKEN']:
        raise exceptions.PermissionDenied("An auth token is required.")

    collections = Collection.objects(private=False).order_by('-vote_count')

    content = dict(
        _links=dict(
            root=url_for('root_api.index', _external=True),
            self=url_for('collections_api.index', _external=True),
        ),
        _items=[serialize(c) for c in collections]
    )

    return content, status.HTTP_200_OK


@blueprint.route("/api/collections/", methods=['POST'])
def create(name=None):
    name = name or request.data.get('name')
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


@blueprint.route("/api/collections/<key>", methods=['PUT'])
def update(key, name=None, code=None, private=None, locked=None):
    collection = Collection.objects(key=key).first()

    if name is None:
        name = request.data.get('name', "")
    if code is None:
        code = request.data.get('code', "")
    if private is None:
        value = request.data.get('private', collection.private)
        private = value not in [False, 'False']
    if locked is None:
        value = request.data.get('locked', collection.locked)
        locked = value not in [False, 'False']

    collection.name = name.strip() or collection.name
    collection.code = code.strip().lower().replace(' ', '-') or collection.code
    collection.private = private
    collection.locked = locked
    collection.save()

    return serialize(collection), status.HTTP_200_OK


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
        code=collection.code,
        private=collection.private,
        locked=collection.locked,
        items=collection.items
    )
