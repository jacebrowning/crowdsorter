import logging
from collections import OrderedDict

from flask import Blueprint, request, url_for
from flask_api import status

from ..models import Collection

from . import _exceptions as exceptions
from ._utils import get_content


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
    log.debug("Parsing request data: %s", request.data)
    name = request.data.get('name')
    try:
        items = request.data.getlist('items')
    except AttributeError:
        # TODO: figure out how to test this automatically
        # it only seems to get triggered from the Flask-API browser
        items = request.data.get('items', [])
    if not name:
        raise exceptions.UnprocessableEntity("Name is required.")

    collection = Collection(name=name, items=items)
    collection.save()

    return get_content(collection), status.HTTP_201_CREATED


@blueprint.route("/api/collections/<key>")
def detail(key):
    collection = Collection.objects(key=key).first()

    if not collection:
        raise exceptions.NotFound

    return get_content(collection), status.HTTP_200_OK


@blueprint.route("/api/collections/<key>/compare", methods=['GET', 'POST'])
def compare(key, winner=None, loser=None):
    collection = Collection.objects(key=key).first()

    if not collection:
        raise exceptions.NotFound

    if request.method == 'POST' or any((winner, loser)):

        winner = winner or request.data.get('winner')
        loser = loser or request.data.get('loser')

        # TODO: record result
        log.debug("Comparison result: %s > %s", winner, loser)

        collection.sort()
        collection.save()

    content = OrderedDict()
    content['name'] = collection.name
    content['items'] = collection.items_shuffled

    return content, status.HTTP_200_OK
