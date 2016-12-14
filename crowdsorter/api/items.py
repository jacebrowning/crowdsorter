import logging

from flask import Blueprint, request
from flask_api import status

from ..models import Collection

from . import _exceptions as exceptions


blueprint = Blueprint('items_api', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/api/collections/<key>/items", methods=['GET', 'POST'])
def detail(key, name=None):
    collection = Collection.objects(key=key).first()

    if not collection:
        raise exceptions.NotFound

    if request.method == 'POST' or name:

        name = name or request.data.get('name')

        if not name:
            raise exceptions.UnprocessableEntity("Name is required.")

        log.debug("Adding to %r: %r", collection, name)
        collection.items.append(name)
        collection.save()

    content = collection.items

    return content, status.HTTP_200_OK
