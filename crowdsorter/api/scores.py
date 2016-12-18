import logging
from collections import OrderedDict

from flask import Blueprint, url_for
from flask_api import status

from ..models import Collection

from . import _exceptions as exceptions


blueprint = Blueprint('scores_api', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/api/collections/<key>/scores")
def index(key):
    collection = Collection.objects(key=key).first()
    if not collection:
        raise exceptions.NotFound

    return serialize(collection), status.HTTP_200_OK


def serialize(collection):
    content = OrderedDict()

    content['_links'] = OrderedDict()
    content['_links']['self'] = url_for(
        '.index', key=collection.key, _external=True)
    content['_links']['collection'] = url_for(
        'collections_api.detail', key=collection.key, _external=True)
    content['name'] = collection.name
    content['item_count'] = collection.item_count
    content['vote_count'] = collection.vote_count
    content['scores'] = [s.data for s in collection.scores]

    return content
