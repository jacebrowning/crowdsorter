import logging
from collections import OrderedDict

from flask import Blueprint, request, url_for
from flask_api import status

from ..models import Collection

from . import _exceptions as exceptions


blueprint = Blueprint('collections_api', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/api/collections/")
def index():
    collections = Collection.objects.order_by('-vote_count')

    content = dict(
        _links=dict(
            root=url_for('root_api.index', _external=True),
            self=url_for('.index', _external=True),
        ),
        _items=[serialize(c) for c in collections]
    )

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


def serialize(collection):
    content = OrderedDict()

    content['_links'] = OrderedDict()
    content['_links']['self'] = url_for(
        'collections_api.detail', key=collection.key, _external=True)
    content['_links']['items'] = url_for(
        'items_api.index', key=collection.key, _external=True)
    content['_links']['votes'] = url_for(
        'votes_api.index', key=collection.key, _external=True)
    content['_links']['scores'] = url_for(
        'scores_api.index', key=collection.key, _external=True)
    content['key'] = collection.key
    content['name'] = collection.name
    content['code'] = collection.code
    content['items'] = collection.items

    return content
