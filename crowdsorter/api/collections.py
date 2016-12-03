import logging

from flask import Blueprint, url_for
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


@blueprint.route("/api/collections/<key>")
def detail(key):
    collection = Collection.objects(key=key).first()

    if not collection:
        raise exceptions.NotFound

    return get_content(collection), status.HTTP_200_OK
