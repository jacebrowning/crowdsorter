import logging
from collections import OrderedDict

from flask import Blueprint
from flask_api import status

from ..models import Collection

from . import _exceptions as exceptions


blueprint = Blueprint('scores_api', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/api/collections/<key>/scores")
def detail(key):
    collection = Collection.objects(key=key).first()

    if not collection:
        raise exceptions.NotFound

    content = OrderedDict()
    content['name'] = collection.name
    content['item_count'] = collection.item_count
    content['vote_count'] = collection.vote_count
    content['scores'] = [s.data for s in collection.scores]

    return content, status.HTTP_200_OK
