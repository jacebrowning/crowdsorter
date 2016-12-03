import logging

from flask import Blueprint
from flask_api import status

# from ..models import Collection

# from . import _exceptions as exceptions
# from ._utils import get_content


blueprint = Blueprint('collections_api', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/api/collections/")
def index():
    return [], status.HTTP_200_OK
